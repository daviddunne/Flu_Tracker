#   Author: David Dunne,    Student Number: C00173649,      Created Mar 2016

import os
"""This file is used to get absolute path to test directory"""

path_to_this_directory = os.path.dirname(__file__)
project_root_dir = path_to_this_directory.replace('/utilities', '')