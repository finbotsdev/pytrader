# encoding: utf-8

import asyncio
import pandas as pd
import pytrader as pt
from pytrader.data import CoinbasePro, CoinbaseProDataFrame
from pytrader.date import date
from pytrader.model import Asset, Exchange, Ohlcv
from pytrader.log import logger
import traceback


"""
c-coinbasepro.py
---------------------
pytrader function template
"""


def main(args):
  print(args)

  try:
    api = CoinbasePro()

    logger.info('get_accounts')
    results = api.get_accounts()

    logger.info('get_currencies')
    results = api.get_currencies()

    logger.info('get_exchange_limits')
    results = api.get_exchange_limits()

    logger.info('get_fees')
    results = api.get_fees()

    logger.info('get_fills')
    results = api.get_fills()

    logger.info('get_orders')
    results = api.get_orders()

    logger.info('get_payment_methods')
    results = api.get_payment_methods()

    logger.info('get_products')
    results = api.get_products()

    logger.info('get_product')
    results = api.get_product('BTC-USD')

    logger.info('get_product_book')
    results = api.get_product_book('BTC-USD')

    logger.info('get_product_ticker')
    results = api.get_product_ticker('BTC-USD')

    logger.info('get_product_trades')
    results = api.get_product_trades('BTC-USD')

    logger.info('get_product_stats')
    sds, dstart = date('2 days ago')
    eds, dend = date('yesterday')
    results = api.get_product_candles_chunked('BTC-USD', dstart, dend)

    print(results)

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
