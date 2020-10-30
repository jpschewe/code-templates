#!/usr/bin/env python3

import warnings
with warnings.catch_warnings():
    import re
    import sys
    import argparse
    import os
    import logging
    import logging.config
    import json
    from pathlib import Path

script_dir=Path(__file__).parent.absolute()

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
    path = Path(default_path)
    value = os.getenv(env_key, None)
    if value:
        path = Path(value)
    if path.exists():
        with open(path, 'r') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


class Base(object):
    def __str__(self):
        return str(self.__dict__)
    
    def __repr__(self):
        type_ = type(self)
        module = type_.__module__
        qualname = type_.__qualname__        
        return f"<{module}.{qualname} {str(self)}>"

    
def main_method(args):
    pass


def multiprocess_logging_handler(logging_queue, logconfig, running):
    import time
    setup_logging(default_path=logconfig)

    def process_queue():
        while not logging_queue.empty():
            try:
                record = logging_queue.get(timeout=1)
                logger = logging.getLogger(record.name)
                logger.handle(record)
            except (multiprocessing.Queue.Empty, multiprocessing.TimeoutError) as e:
                # timeout was hit, just return
                pass
        
    while running.value > 0:
        process_queue()

    # process any last log messages
    process_queue()

    
def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    class ArgumentParserWithDefaults(argparse.ArgumentParser):
        '''
        From https://stackoverflow.com/questions/12151306/argparse-way-to-include-default-values-in-help
        '''
        def add_argument(self, *args, help=None, default=None, **kwargs):
            if help is not None:
                kwargs['help'] = help
            if default is not None and args[0] != '-h':
                kwargs['default'] = default
                if help is not None:
                    kwargs['help'] += ' (default: {})'.format(default)
            super().add_argument(*args, **kwargs)
        
    parser = ArgumentParserWithDefaults(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-l", "--logconfig", dest="logconfig", help="logging configuration (default: logging.json)", default='logging.json')
    parser.add_argument("--debug", dest="debug", help="Enable interactive debugger on error", action='store_true')

    args = parser.parse_args(argv)

    if 'multiprocessing' in sys.modules:
        running = multiprocessing.Value('b', 1)
        logging_queue = multiprocessing.Queue()
        logging_listener = multiprocessing.Process(target=multiprocess_logging_handler, args=(logging_queue, args.logconfig,running,))
        logging_listener.start()

        h = logging.handlers.QueueHandler(logging_queue)
        root = logging.getLogger()
        root.addHandler(h)
        root.setLevel(logging.DEBUG)
    else:
        logging_listener = None
        setup_logging(default_path=args.logconfig)

    try:
        if args.debug:
            import pdb, traceback
            try:
                return main_method(args)
            except:
                extype, value, tb = sys.exc_info()
                traceback.print_exc()
                pdb.post_mortem(tb)    
        else:
            return main_method(args)
    finally:
        if logging_listener:
            running.value = 0
        
            
if __name__ == "__main__":
    sys.exit(main())
