#!/usr/bin/env python

from pytrader.log import logger
import pytrader.screener as screener

"""
  screener
  ------
  query symbols to watch using stored procedure queries

  usage:
  ------
  tickers=$(pytrade screener); echo $tickers
"""


def argparser(subparser):
  parser = subparser.add_parser('screener')
  parser.add_argument('-s', '--strategy', default='s&p500', help="the strategy filter to use for the screener" )


def main(args):
  logger.debug('pytrader screener')
  logger.debug(args)

  strategy = args.strategy

  logger.debug(f'fetching symbols to watch using strategy {strategy}')
  search = screener.Search(strategy)
  symbols = search.symbols()
  print(" ".join(symbols))

