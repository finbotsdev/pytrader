# -*- coding: utf-8 -*-

from pytrader.log import logger

from .assets import main as assets
from .exchanges import main as exchanges
from .etfholdings import main as etfholdings
from .wallstreetbets import main as wallstreetbets

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

  eval(args.resource+'(args)')
