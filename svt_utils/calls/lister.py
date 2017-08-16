'''
This software may contain the intellectual property of EMC Corporation or be
licensed to EMC Corporation from third parties. Use of this software and the
intellectual property contained therein is expressly limited to the terms and
conditions of the License Agreement under which it is provided by or on behalf
of EMC. This code is provided AS IS, without warranty of any kind express or
implied.
'''

import sys
from svt_lib.wrapper import Wrapper
from svt_lib.errors import Errors
import svt_cfg.config

__author__ = "David CLAUVEL"
__version__ = "0.1"
__status__ = "Concept Code"


# Globals
# Import module globals
settings = svt_cfg.config.NORMAL_SETTINGS


def main():

    res = Wrapper().lister(settings)
    print(res)


if __name__ == '__main__':

    # Generate
    try:
        main()
    except Errors.genError as e:
        print(e.msg)
        sys.exit(e.code)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
