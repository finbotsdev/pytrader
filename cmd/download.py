#!/usr/bin/env python

import os
from pytrader.data import YahooFinance
from pytrader.database import Session
from pytrader.date import date
from pytrader.log import logger
from pytrader.model import Asset


"""
  download
  ------
  download historical data for assets
  currenlty only supports downloads from yahoo finance
"""


def argparser(subparser):
  parser = subparser.add_parser('download')
  parser.add_argument("-e", "--end", default="yesterday", help="earliest date to include")
  parser.add_argument("-i", "--interval", default="day", help="market data aggregation level (day or minute)")
  parser.add_argument("-s", "--start", default="5 years ago", help="latest date to include")
  parser.add_argument('-t', '--tickers', default=[], help="list of ticker symbols to include", nargs='+' )


def main(args):
  logger.debug('pytrader download')
  logger.debug(args)

  eds, dend = date(args.end)
  interval = args.interval
  sds, dstart = date(args.start)
  tickers = args.tickers

  api = YahooFinance()
  session = Session()

  if not tickers: # if no tickers provided fetch all from database
    assets = session.query(Asset.symbol).filter(
      Asset.status == 'active',
      Asset.is_tradeable == True
    ).all()
    tickers = [a.symbol for a in assets]

  intervals = { # map param interval to what yfinance expects
    'minute': '1m',
    'day': '1d'
  }

  for s in tickers: # iterate tickers and fetch historical data
    logger.info(f'fetching market data ({interval}) for {s} beginning {sds} and ending {eds}')
    for ticker in tickers:
      api.set_symbol(ticker)
      df = api.history(end = dend, interval = intervals[interval], start = dstart )
      os.makedirs(f'./.data/{interval}', exist_ok=True)
      df.to_csv(f'./.data/{interval}/{s}.csv')
