# -*- coding: utf-8 -*-

from pytrader.log import logger
from pytrader.data import AlpacaStream


"""
  stream
  ------
"""


def argparser(subparser):
  parser = subparser.add_parser('stream')
  parser.add_argument('-t', '--tickers', default=[], help="list of ticker symbols to include", nargs='+' )


def main(args):
  logger.debug('pytrader stream')
  logger.debug(args)

  ws = AlpacaStream()
  ws.set_tickers(args.tickers)
  ws.run()
