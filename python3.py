#!/usr/bin/env python3.6

import warnings
with warnings.catch_warnings():
    import re
    import sys
    import argparse
    import os
    import os.path
    import logging
    import logging.config
    import json
    from pathlib import Path

script_dir=os.path.abspath(os.path.dirname(__file__))

def get_logger():
    return logging.getLogger(__name__)

def setup_logging(
    default_path='logging.json',
    default_level=logging.INFO,
    env_key='LOG_CFG'
):
    """
    Setup logging configuration
    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'r') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

def create_preferences_directory():
    if os.name != "posix":
        from win32com.shell import shellcon, shell
        homedir = "{}\\".format(shell.SHGetFolderPath(0, shellcon.CSIDL_APPDATA, 0, 0))
    else:
        homedir = "{}/".format(os.path.expanduser("~"))

    projectname = "test"
    if not os.path.isdir("{0}.{1}".format(homedir,projectname)):
        os.makedirs("{0}.{1}".format(homedir,projectname))

class Base(object):
    def __str__(self):
        return str(self.__dict__)
    
    def __repr__(self):
        type_ = type(self)
        module = type_.__module__
        qualname = type_.__qualname__        
        return f"<{module}.{qualname} {str(self)}>"

        
def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--logconfig", dest="logconfig", help="logging configuration (default: logging.json)", default='logging.json')

    args = parser.parse_args(argv)

    setup_logging(default_path=args.logconfig)
    
        
if __name__ == "__main__":
    sys.exit(main())
    
