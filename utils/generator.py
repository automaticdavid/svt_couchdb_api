"""
This software may contain the intellectual property of EMC Corporation or be
licensed to EMC Corporation from third parties. Use of this software and the
intellectual property contained therein is expressly limited to the terms and
conditions of the License Agreement under which it is provided by or on behalf
of EMC. This code is provided AS IS, without warranty of any kind express or
implied.
"""

import sys
from optparse import OptionParser
import simplejson as json
from lib.wrapper import Wrapper
from lib.errors import Errors
import cfg.config

__author__ = "David CLAUVEL"
__version__ = "1.1"
__status__ = "Concept Code"


# Import module globals
settings = cfg.config.NORMAL_SETTINGS


def main(settings, collect, client):

    res = Wrapper().generator(settings, collect, client, yamldef)
    print(json.dumps(json.loads(res), indent=4, sort_keys=True))


if __name__ == '__main__':

    # Argument parser
    parser = OptionParser()
    parser.add_option(
        "-s", "--solutionid",
        dest='client',
        help="Name of the client or solutionid value")
    parser.add_option(
        "-c", "--collect",
        dest='collect',
        help="Date of the collect as: 2016-09-12-11-45-45")
    parser.add_option(
        "-y", "--yamldef",
        dest='yamldef',
        help="YAML definition for this generator run")

    (options, args) = parser.parse_args()

    # Set parsed values
    collect = options.collect
    client = options.client
    yamldef = options.yamldef

    # Test input
    if not client:
        msg = "Error: specifiying the client with -s is required"
        sys.exit(msg)
    if not collect:
        msg = "Error: specifiying a collect date with -c YYYY-MM-DD-HH-MM-SS"
        msg += " is required"
        sys.exit(msg)
    if not yamldef:
        msg = "Error: specifiying a YAML file with -y is required"
        sys.exit(msg)

    # Test files
    try:
        open(yamldef)
    except IOError:
        sys.exit("Error: can't read yaml file: " + yamldef)
    try:
        open(settings)
    except IOError:
        sys.exit("Error: can't read settings file: " + settings)

    # Generate
    try:
        main(settings, collect, client)
    except Errors.genError as e:
        print(e.msg)
        sys.exit(e.code)
    except Errors.svtError as e:
        print(e.code)
        print(e.msg)
        print(e.call)
        sys.exit(e.code)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
