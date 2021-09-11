# encoding: utf-8

import os
import pandas as pd
import pytrader as pt
from pytrader.data import AlpacaMarkets, AlpacaDataframe
from pytrader.log import logger
import traceback


"""
alpaca.py
---------------------
download ohclv data from alpaca markets

"""


def main(symbol: str, interval: str, start, end):
  """
  :param symbol: str
  :param interval: str
  :param start: str
  :param end: str
  """
  try:
    logger.debug('pytrader alpaca download')
    logger.debug(f'{symbol} {interval} {start} {end}')

    api = AlpacaMarkets()

    datadir = f'./.data/minute'
    datafile = f'.data/minute/{symbol}.csv'

    intervals = { # map param interval to what yfinance expects
      'minute': '1Min',
      'hour': '1Hour',
      'day': '1Day'
    }

    os.makedirs(datadir, exist_ok=True)
    bars = api.get_bars_chunked(symbol=symbol, end=end, start=start, timeframe=intervals[interval])

    if bars:
      df = AlpacaDataframe(bars)

      # if datafile exists
      if os.path.isfile(datafile):
        df1 = pd.read_csv(datafile)
        df1.reset_index()
        df1['dt'] = pd.to_datetime(df1['dt'])
        df = df.append(df1)

      df.drop_duplicates('dt', inplace=True)
      df.sort_values('dt', axis=0, inplace=True)
      df.set_index('dt', inplace=True)
      df.to_csv(datafile)

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
