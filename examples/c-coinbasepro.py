# encoding: utf-8

import pytrader as pt
from pytrader.data import CoinbasePro
from pytrader.log import logger
import traceback
from datetime import datetime


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
    results = api.get_product_candles('BTC-USD')
    # for candle in results:
    #   closetime = int(candle[0])
    #   ct = datetime.fromtimestamp(closetime)
    #   candle[0] = ct
    #   print(candle)

    logger.info('get_product_stats')
    results = api.get_product_stats('BTC-USD')

    logger.info('get_profiles')
    results = api.get_profiles()

    logger.info('get_reports')
    results = api.get_reports()

    logger.info('get_time')
    results = api.get_time()

    logger.info('get_transfers')
    results = api.get_transfers()

    logger.info('get_user_verify')
    results = api.get_user_verify()

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
