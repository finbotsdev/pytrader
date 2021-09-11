# -*- coding: utf-8 -*-

from pytrader.log import logger

from .alpaca import main as alpaca
from .coinbasepro import main as coinbasepro
from .cryptowatch import main as cryptowatch


"""
  stream
  ------
"""


def argparser(subparser):
  parser = subparser.add_parser('stream')
  parser.add_argument('-s', '--source', help="stream source (alpaca|coinbase)" )
  parser.add_argument('-t', '--tickers', default=[], help="list of ticker symbols to include", nargs='+' )


def main(args):
  logger.info('pytrader stream')
  logger.info(args)

  if args.source == 'alpaca':
    alpaca(args)

  if args.source == 'coinbasepro':
    coinbasepro(args)

  if args.source == 'cryptowatch':
    cryptowatch(args)

