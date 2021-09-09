# encoding: utf-8

from model import engine
import pandas as pd
import pytrader as pt
from pytrader.data import AlpacaMarkets
from pytrader.date import date
from pytrader.log import logger
from model import engine
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
    df = api.get_bars_chunked('AAPL', end=eds, start=sds)
    print(df)

    # # this is fantastically fast but fails on duplicate recores
    # # dataframe to_sql will fail if uniqueness indexes fail
    # df.to_sql('ohlcv', engine, if_exists='append', index=False)

    # iterate dataframe and check for duplicate rows before writing
    # ignores duplicates but is very slow
    for i, row in df.iterrows():
      try:
        df.iloc[i:i+1].to_sql(con=engine, if_exists='append', index=False, name="ohlcv")
      except Exception as e:
        pass

    # possible solutions
    # https://gist.github.com/Nikolay-Lysenko/0887f4b59dc4914cec9b236c317d06e3
    # https://gist.github.com/luke/5697511

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
