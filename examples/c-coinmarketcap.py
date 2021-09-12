# encoding: utf-8

import asyncio
import pandas as pd
import pytrader as pt
from pytrader.data import CoinmarketcapPro
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
    api = CoinmarketcapPro()

    logger.info('get_crypto_map')
    results = api.get_crypto_map()

    logger.info('get_crypto_info')
    results = api.get_crypto_info('BTC,ETH,LTC')

    logger.info('get_crypto_listings_latest')
    results = api.get_crypto_listings_latest()

    logger.info('get_crypto_categories')
    results = api.get_crypto_categories()

    logger.info('get_crypto_trending_latest')
    results = api.get_crypto_trending_latest()


    print(results)
    print(type(results))
    for record in results['data']:
      print(record)

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
