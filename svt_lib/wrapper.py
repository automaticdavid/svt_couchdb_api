"""
This software may contain the intellectual property of EMC Corporation or be
licensed to EMC Corporation from third parties. Use of this software and the
intellectual property contained therein is expressly limited to the terms and
conditions of the License Agreement under which it is provided by or on behalf
of EMC. This code is provided AS IS, without warranty of any kind express or
implied.
"""

import logging
import os
import yaml
import simplejson as json
from svt_lib.utils import Utils
from svt_lib.config import Readconfig
from svt_lib.couch import Couch
from svt_lib.errors import Errors
from svt_lib.svt import Svt
import svt_cfg.config

__author__ = "David CLAUVEL"
__version__ = "1.1"
__status__ = "Concept Code"

# Module level logger
logger = logging.getLogger(__name__)

# Import module globals
settings = svt_cfg.config.NORMAL_SETTINGS
yamldefs = svt_cfg.config.YAML_DEFS


class Wrapper:

    # Load zip file content into CouchDB
    def loader(self, settings, f, client):

        # Init connections parameters
        cfg = Readconfig().readconfig(settings)

        # Init couch connection
        couch = Couch(cfg)

        # Test Welcome
        j = couch.isAlive()
        print('Is Alive ? ' + j)

        # Check if SVT DB exists
        if not couch.hasDB():
            code = 99
            msg = "Missing or wrong SVT database: " + cfg.db
            call = cfg.url
            debug = cfg
            raise Errors.genError(code, msg, call, debug)

        # Parsed arguments
        print('Action: Load')
        print('File: ' + f.filename)
        print('Client: ' + client)

        # Extract collect from zip filename
        fullname = os.path.basename(f.filename)
        name = os.path.splitext(fullname)[0]
        collect = name.replace('output_svt_', '')

        # Check if collect already in Couch using reduce grouping at 2
        startkey = [collect, client]
        endkey = [collect, client, {}]
        print("Checking for collect pre existence")
        r = couch.getReduce(
            'admin',
            'isnewcollect',
            startkey=startkey,
            endkey=endkey,
            group='2')
        new = json.loads(r)
        if new['rows']:
            code = 99
            msg = "Client: " + client
            msg += " already has a collect for date: " + collect
            call = "admin/isnewcollect"
            debug = [startkey, endkey, r, new]
            raise Errors.genError(code, msg, call, debug)

        # Decorate and create bulk json
        bulk = {}
        bulk['docs'] = []
        warnings = []
        d = Utils().decorator(f, client)
        for k, s in d.items():
            try:
                j = json.loads(s)
                bulk['docs'].append(j)
            except ValueError:
                warnings.append("Invalid JSON for CouchDB in file: " + k)
                raise

        # List the invalid files
        print("\n".join(warnings))

        # Bulk load
        try:
            data = json.dumps(bulk)
            couch.postBulk(data)
            return({'svt_upload': 'OK', 'client': client, 'date': collect})
        except:
            print("Error with bulk loader")
            raise

    # Generate JSON from CouchDB and report def YAML
    def generator(self, settings, collect, client, yamldef):

        # Init connections parameters
        cfg = Readconfig().readconfig(settings)

        # Init couch connection
        couch = Couch(cfg)

        # Test Welcome
        j = couch.isAlive()
        print(j)

        # Check if SVT DB exists
        if not couch.hasDB():
            code = 99
            msg = "Missing or wrong SVT database: " + cfg.db
            call = 'hasDB'
            debug = cfg
            raise Errors.genError(code, msg, call, debug)

        # Parsed arguments
        print('Action: Generate')
        print('Collect: ' + collect)
        print('Client: ' + client)
        print('YAML: ' + yamldef)

        # Check if collect already in Couch using reduce grouping at 2
        startkey = [collect, client]
        endkey = [collect, client, {}]
        print("Checking for collect existence")
        r = couch.getReduce(
            'admin',
            'isnewcollect',
            startkey=startkey,
            endkey=endkey,
            group='2')
        new = json.loads(r)
        if not new['rows']:
            code = 99
            msg = "Client: " + client
            msg += " does not have a collect for date: " + collect
            call = "admin/isnewcollect"
            debug = [startkey, endkey, r, new]
            raise Errors.genError(code, msg, call, debug)

        # Parse YAML
        h = open(yamldef)
        y = yaml.load(h)
        reports = Utils().flatten(y)

        # Structure for result json
        res = Utils().hash()

        # Call couch for reports
        for (view, selector), markers in reports.items():

            # Key passed to the  view: will select only given collect & client
            startkey = [collect, client]
            endkey = [collect, client, {}]
            c = couch.getView(view, selector, startkey, endkey)
            r = Utils().cleanKeys(c)

            # Loop over the markers
            for marker in markers:
                # Save the Caller
                caller = [client, collect, view, selector, marker]
                # Deal with the catch all special marker
                if marker == 'svt_all':
                    hook = Svt(selector=selector).hook_all
                    j = json.loads(
                        r,
                        object_hook=hook)
                else:
                    hook = Svt(
                        selector=selector,
                        marker=marker).hook_marker
                    j = json.loads(
                        r,
                        object_hook=hook)
                # Special ViPR call
                if 'vipr' in view:
                    pass
                # Update hash result
                res = Utils().jsonify(res, caller, j)

        # Dump the hash into a json string
        if not res:
            res = {'svt_no_data': 'svt_no_data'}
        return(res)

    # List all clients and collects from the Couch
    def lister(self, settings):

        # Init connections parameters
        cfg = Readconfig().readconfig(settings)

        # Init couch connection
        couch = Couch(cfg)

        # Test Welcome
        j = couch.isAlive()
        print(j)

        # Check if SVT DB exists
        if not couch.hasDB():
            code = 99
            msg = "Missing or wrong SVT database: " + cfg.db
            call = cfg.url
            debug = cfg
            raise Errors.genError(code, msg, call, debug)

        # Call reduce
        r = couch.getReduce(
            'admin',
            'isnewcollect',
            startkey=None,
            endkey=None,
            group='2')
        j = json.loads(r)

        # Do some formating
        res = {}
        for row in j['rows']:
            k = row['key']
            (date, client) = k
            if client in res:
                res[client].append(date)
            else:
                res[client] = [date]
        return res

    def deleter(self, settings, collect, client):

        # Init connections parameters
        cfg = Readconfig().readconfig(settings)

        # Init couch connection
        couch = Couch(cfg)

        # Test Welcome
        j = couch.isAlive()
        print('Is Alive ? ' + j)

        # Check if SVT DB exists
        if not couch.hasDB():
            code = 99
            msg = "Missing or wrong SVT database: " + cfg.db
            call = cfg.url
            debug = cfg
            raise Errors.genError(code, msg, call, debug)

        # Parsed arguments
        print('Action: Delete')
        print('date: ' + collect)
        print('Client: ' + client)

        #  Get those docs
        startkey = [collect, client]
        endkey = [collect, client, {}]
        print("Finding collect docs")
        r = couch.getViewIncludeDocs(
            'admin',
            'isnewcollect',
            startkey=startkey,
            endkey=endkey)
        docs = json.loads(r)

        # Check for existence
        if not docs['rows']:
            code = 99
            msg = "Collect does not exist"
            call = [client, collect]
            debug = r
            raise Errors.genError(code, msg, call, debug)

        # Build the bulk delete JSON
        deleted = []
        for doc in docs['rows']:
            cid = doc["doc"]["_id"]
            crev = doc["doc"]["_rev"]
            ccollect = doc["doc"]["svt_collect_date"]
            cclient = doc["doc"]["svt_client"]
            # Sanity check the key filter
            if ccollect != collect or cclient != client:
                code = 99
                msg = "View result gives different client"
                call = [client, collect, cclient, ccollect]
                debug = r
                raise Errors.genError(code, msg, call, debug)
            deleted.append({"_id": cid, "_rev": crev, "deleted": "true"})

        d = {"docs": deleted}

        # Bulk delete
        try:
            data = json.dumps(d)
            couch.postBulk(data)
            return {"svt_delete": "OK"}
        except:
            print("Error with bulk delete")
            raise

    # List all the available yamldefs in a friendly format
    def reportlister(self):
        res = {}
        for yamldef in os.listdir(yamldefs):
            try:
                ddoc, yamlname = yamldef.split("_")
                view = os.path.splitext(yamlname)[0]
                if ddoc in res:
                    res[ddoc].append(view)
                else:
                    res[ddoc] = [view]
            except:
                pass
        return res
