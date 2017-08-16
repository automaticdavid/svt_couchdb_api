"""
This software may contain the intellectual property of EMC Corporation or be
licensed to EMC Corporation from third parties. Use of this software and the
intellectual property contained therein is expressly limited to the terms and
conditions of the License Agreement under which it is provided by or on behalf
of EMC. This code is provided AS IS, without warranty of any kind express or
implied.
"""

import os

__author__ = "David CLAUVEL"
__version__ = "1.1"
__status__ = "Concept Code"

# Globals
SETTINGS_FILE_NAME = 'config.cfg'
ADMIN_FILE_NAME = 'admin.cfg'
YAML_DIR = 'yaml'
OS_PATH = os.path.dirname(os.path.realpath(__file__))
ROOT_PATH = os.path.dirname(OS_PATH)
NORMAL_SETTINGS = OS_PATH + '/' + SETTINGS_FILE_NAME
ADMIN_SETTINGS = OS_PATH + '/' + ADMIN_FILE_NAME
YAML_DEFS = ROOT_PATH + '/' + YAML_DIR
