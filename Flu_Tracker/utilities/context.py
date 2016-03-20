import os
"""This file is used to get absolute path to test directory"""

dir = os.path.dirname(__file__)
project_root_dir = dir.replace('/utilities', '')