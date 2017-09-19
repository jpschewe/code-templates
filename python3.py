#!/usr/bin/env python3

import warnings
with warnings.catch_warnings():
    import re
    import sys
    import argparse
    import os
    import os.path
    import logging

script_dir=os.path.abspath(os.path.dirname(__file__))
    
def create_preferences_directory():
    if os.name != "posix":
        from win32com.shell import shellcon, shell
        homedir = "{}\\".format(shell.SHGetFolderPath(0, shellcon.CSIDL_APPDATA, 0, 0))
    else:
        homedir = "{}/".format(os.path.expanduser("~"))

    projectname = "test"
    if not os.path.isdir("{0}.{1}".format(homedir,projectname)):
        os.makedirs("{0}.{1}".format(homedir,projectname))
    
def main(argv=None):
    logging.basicConfig(level=logging.INFO)
    
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--logfile", dest="logfile", help="logfile", required=True)

    args = parser.parse_args(argv)

    for a in args[1:]:
        pass
        
if __name__ == "__main__":
    sys.exit(main())
    
