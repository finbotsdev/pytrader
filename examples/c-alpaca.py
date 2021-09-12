# encoding: utf-8

import pandas as pd
import pytrader as pt
from pytrader.data import AlpacaMarkets, AlpacaDataframe
from pytrader.date import date
from pytrader.log import logger
import traceback


"""
c-alpaca.py
---------------------
pytrader function template
"""


def main(args):
  print(args)

  try:

    sds, dstart = date('2 days ago')
    eds, dend = date('yesterday')

    api = AlpacaMarkets()

    logger.info('get_account')
    results = api.get_account()

    logger.info('get_assets')
    results = api.get_assets()

    logger.info('get_calendar')
    results = api.get_calendar(end=eds, start=sds)

    logger.info('get_clock')
    results = api.get_clock()

    logger.info('get_watchlists')
    results = api.get_watchlists()

    logger.info('get_bars')
    results = api.get_bars_chunked('AAPL', end=eds, start=sds)

    for item in results:
      print(item)


  except Exception as e:
    logger.error(e)
    print(e)
    print(traceback.format_exc())


if __name__ == '__main__':
  parser = pt.ArgumentParser()
  parser.add_argument("-v", "--verbose", action='store_true', help="verbose")
  args = parser.parse_args()

  timer = pt.Timer()
  logger.info(f'pytrader {__file__}')
  main(args)
  timer.report()
