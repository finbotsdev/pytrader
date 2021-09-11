# -*- coding: utf-8 -*-

from pytrader.database import Session
from pytrader.date import date
from pytrader.log import logger
from pytrader.model import Asset

from .alpaca import main as alpaca
from .coinbasepro import main as coinbasepro
from .yfinance import main as yfinance

"""
  download
  ------
  download historical data for assets
  save data to .data directory as csv
"""


def argparser(subparser):
  parser = subparser.add_parser('download')
  parser.add_argument("-e", "--end", default="yesterday", help="earliest date to include")
  parser.add_argument("-i", "--interval", default="day", help="market data aggregation level (day or minute)")
  parser.add_argument("-s", "--start", default="5 years ago", help="latest date to include")
  parser.add_argument('-t', '--tickers', default=[], help="list of ticker symbols to include", nargs='+' )


def main(args):
  logger.info('pytrader download')
  logger.info(args)

  eds, dend = date(args.end)
  interval = args.interval
  sds, dstart = date(args.start)
  tickers = args.tickers

  session = Session()

  # if no tickers provided fetch all from database
  if tickers:
    assets = session.query(Asset).filter(
      Asset.symbol.in_(tickers)
    ).all()
  else:
    assets = session.query(Asset).filter(
      Asset.status.in_(['active', 'online'])
    ).all()

  for asset in assets:
    print(asset)

    if asset.asset_class == 'digital':
      """
      if the requested asset is digital - use coinbasepro
      """
      coinbasepro(asset.symbol, interval, sds, eds)

    else:

      if interval == 'day':
        """
        if the requested asset is not digital and the interval is day - use yfinance
        """
        yfinance(asset.symbol, interval, dstart, dend)

      else:
        """
        if the requested asset is not digital and the interval is minute - use alpaca
        """
        alpaca(asset.symbol, interval, sds, eds)
