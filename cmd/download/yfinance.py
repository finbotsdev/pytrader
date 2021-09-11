# encoding: utf-8

from datetime import datetime
import os
import pytrader as pt
from pytrader.data import YahooFinance
from pytrader.log import logger
import traceback


"""
yfinance.py
---------------------
download ohclv data from yahoo finance

"""


def main(symbol: str, interval: str, start, end):
  """
  :param symbol: str
  :param interval: str
  :param start: datetime
  :param end: datetime
  """
  try:
    logger.debug('pytrader yfinance download')

    api = YahooFinance()

    intervals = { # map param interval to what yfinance expects
      'minute': '1m',
      'day': '1d'
    }

    logger.info(f'fetching market data ({interval}) for {symbol} beginning {start} and ending {end}')
    api.set_symbol(symbol)
    df = api.history(end = end, interval = intervals[interval], start = start )
    os.makedirs(f'./.data/{interval}', exist_ok=True)
    df.to_csv(f'./.data/{interval}/{symbol}.csv')

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
