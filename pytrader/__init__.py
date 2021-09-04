from .hello import Hello  # noqa
import argparse
import pytrader.log as log
import sys
import time

__version__ = '0.1.0'

logger = log.logging
log.config_root_logger()


class ArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

class Timer():
    def __init__(self):
        self.start_time = time.time()

    def report(self):
        logger.info(f'--- {time.time() - self.start_time} seconds ---')
