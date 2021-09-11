# encoding: utf-8

import os
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
    api = AlpacaMarkets()

    symbols = ['AAPL', 'MSFT','TSLA']
    latest = 'today'
    earliest = '1 year ago'

    for symbol in symbols:
      datadir = f'./.data/minute'
      datafile = f'.data/minute/{symbol}.csv'

      os.makedirs(datadir, exist_ok=True)

      sds, dstart = date(earliest)
      eds, dend = date(latest)
      bars = api.get_bars_chunked(symbol=symbol, end=eds, start=sds)

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
