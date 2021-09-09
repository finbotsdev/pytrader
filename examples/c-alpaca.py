# encoding: utf-8

import pytrader as pt
from pytrader.data import AlpacaMarkets
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
    api = AlpacaMarkets()

    logger.info('get_account')
    print(api.get_account())

    logger.info('get_assets')
    print(api.get_assets())

    logger.info('get_calendar')
    print(api.get_calendar(end=date('yesterday'), start=date('one week ago')))

    logger.info('get_clock')
    print(api.get_clock())

    logger.info('get_watchlists')
    print(api.get_watchlists())

    logger.info('get_bars')

    # convert string dates to datetime objects
    sds, dstart = date('1 month ago')
    eds, dend = date('yesterday')
    print(api.get_bars_chunked('AAPL', end=eds, start=sds))

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
