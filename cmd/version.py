# -*- coding: utf-8 -*-

import ast
from pytrader.log import logger
import re


"""
  version
  ------
  display version information
"""


def argparser(subparser):
  parser = subparser.add_parser('version')


def main(args):
  logger.debug('pytrader version')
  logger.debug(args)

  _version_re = re.compile(r'__version__\s+=\s+(.*)')
  with open('pytrader/__init__.py', 'rb') as f:
      version = str(ast.literal_eval(_version_re.search(
          f.read().decode('utf-8')).group(1)))
  print(f'pytrader library version {version}')

def argparse():
  pass
