# -*- coding: utf-8 -*-

import os
from pytrader.log import logger


"""
  sync
  ------

"""


def argparser(subparser):
  parser = subparser.add_parser('sync')
  parser.add_argument('-r', '--resource', default='stock', help="resource type to sync" )


def main(args):
  logger.debug('pytrader assets')
  logger.debug(args)
  os.system(f'python sync/{args.resource}.py')
