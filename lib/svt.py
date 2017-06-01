"""
This software may contain the intellectual property of EMC Corporation or be
licensed to EMC Corporation from third parties. Use of this software and the
intellectual property contained therein is expressly limited to the terms and
conditions of the License Agreement under which it is provided by or on behalf
of EMC. This code is provided AS IS, without warranty of any kind express or
implied.
"""

__author__ = "David CLAUVEL"
__version__ = "1.1"
__status__ = "Concept Code"


class Svt:

    def __init__(self, **kw):
        self.__dict__.update(kw)

    # Used for json.loads object_hook
    def hook_marker(self, d):

        selector = self.selector
        marker = self.marker

        # Outer nest json has 'svt_cdb_key', enforced by CouchDB views
        if 'svt_cdb_key' not in d:
            return(d)

        # Get the selected subjson & action
        selected = d['svt_cdb_value'][selector]
        action = d['svt_cdb_value']['svt_action']

        # Special case for keyed svt_group
        if (
                isinstance(selected, dict) and
                marker in selected and
                isinstance(selected[marker], list) and
                action == 'svt_group'
        ):
            s = selected[marker]
            special = True
        else:
            s = selected
            special = False

        # Normal dict
        if isinstance(s, dict) and marker in s:
            v = s[marker]

        # Simple string attach
        elif isinstance(s, str):
            v = s

        # Is it a list ?
        # Each item has been keyed with 'svt_unic' by the view
        elif isinstance(s, list):
            v = {}
            for i in s:
                # Get the marked value
                if 'svt_unic' not in i or 'svt_value' not in i:
                    msg = 'Map function for does not re-key lists for selector'
                    msg += ': ' + selector
                    raise Exception(msg)
                elif special:
                    marked = i['svt_value']
                elif marker not in i['svt_value']:
                    marked = 'svt_no_data'
                else:
                    marked = i['svt_value'][marker]
                # Gracefully manage errors in map
                svt_unic = i['svt_unic']
                if svt_unic not in v:
                    v[svt_unic] = marked
                    v['svt_marked'] = True
                else:
                    msg = 'Map function for selector: ' + selector
                    msg += ' uses non unique key'
                    raise Exception(msg)

        # Selected subjson is empty
        else:
            v = 'svt_no_data'

        # Add the key to the result
        (collect, client, source, name) = d['svt_cdb_key']

        # Output object
        r = {
                'collect': collect,
                'client': client,
                'source': source,
                'name': name,
                'action': action,
                'value': v
            }
        return Svt(**r)

    # Used for json.loads object_hook
    # Get all first level markers
    def hook_all(self, d):

        selector = self.selector

        # Outer nest json has 'svt_cdb_key', enforced by CouchDB views
        if 'svt_cdb_key' not in d:
            return(d)

        # Get the selected subjson, action and marked id
        selected = d['svt_cdb_value'][selector]
        action = d['svt_cdb_value']['svt_action']
        if 'svt_marked' in d['svt_cdb_value']:
            marked = d['svt_cdb_value']['svt_marked']
        else:
            marked = False

        # Special case for keyed svt_group
        if (
                isinstance(selected, dict) and
                marked and
                isinstance(selected[marked], list) and
                action == 'svt_group'
        ):
            s = selected[marked]
        else:
            s = selected

        # Simple attach of everything
        if isinstance(s, dict) or isinstance(s, str):
            v = s

        # Is it a list ?
        # Each item has been keyed with 'svt_unic' by the view
        elif not isinstance(s, str):
            v = {}
            for i in s:
                # Get the marked value
                if 'svt_unic' not in i or 'svt_value' not in i:
                    msg = 'Map function for does not re-key lists for selector'
                    msg += ': ' + selector
                    raise Exception(msg)
                else:
                    svt_unic = i['svt_unic']
                    marked = i['svt_value']
                # Gracefully manage errors in map
                if svt_unic not in v:
                    v[svt_unic] = marked
                    v['svt_marked'] = True
                else:
                    msg = 'Map function for selector: '
                    msg += selector + ' uses non unique key'
                    raise Exception(msg)

        # Selected subjson is empty
        else:
            v = {'svt_no_data': 'svt_no_data'}

        # Add the key to the result
        (collect, client, source, name) = d['svt_cdb_key']

        # Output object
        r = {
                'collect': collect,
                'client': client,
                'source': source,
                'name': name,
                'action': action,
                'value': v
            }
        return Svt(**r)
