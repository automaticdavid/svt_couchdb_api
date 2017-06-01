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
from lib.wrapper import Wrapper
from lib.errors import Errors
import cfg.config

__author__ = "David CLAUVEL"
__version__ = "1.1"
__status__ = "Concept Code"


# Import module globals
settings = cfg.config.NORMAL_SETTINGS


def main(f, client):

    Wrapper().loader(settings, f, client)


if __name__ == '__main__':

    # Argument parser
    parser = OptionParser()
    parser.add_option(
        "-f", "--file",
        dest='loadfile',
        help="Collect ZIP file")
    parser.add_option(
        "-c", "--client",
        dest='client',
        help="Name of the client")
    (options, args) = parser.parse_args()

    # Set parsed values
    loadfile = options.loadfile
    client = options.client

    # Test arguments
    if not client:
        sys.exit("Error: specifiying the client with -c is required")
    if not loadfile:
        sys.exit("Error: specifiying a file to load with -f is required")

    # Test files
    try:
        open(settings)
    except IOError:
        sys.exit("Error: can't read settings file: " + settings)
    try:
        open(loadfile)
    except IOError:
        sys.exit("Error: can't read collect zip file: " + loadfile)

    # Load
    try:
        main(loadfile, client)
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
