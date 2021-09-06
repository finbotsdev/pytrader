# encoding: utf-8

import ccxt
import pandas as pd
import pytrader as pt
import pytrader.config as cfg
from pytrader.log import logger


"""
c-ccxt.py
---------------------
query coinbase pro data using ccxt
"""


def main(args):
  print(args)

  try:
    logger.info('doing a thing')

    # print a list of all available exchange classes
    # print(ccxt.exchanges)

    exchange = ccxt.coinbasepro({
      'apiKey': cfg.get('COINBASEPRO_API_KEY_ID'),
      'secret': cfg.get('COINBASEPRO_API_SECRET_KEY'),
      'password': cfg.get('COINBASEPRO_API_PASSWORD'),
      'TIMEOUT': 30000,
      'enableRateLimit': True
    })

    logger.info('exchange')
    print(exchange)

    logger.info('fetch_balance')
    balances = exchange.fetch_balance()

    logger.info('load_markets')
    markets = exchange.load_markets()

    logger.info('fetch_ohlcv')
    bars = exchange.fetch_ohlcv('ADA/USD', timeframe='1m', limit=30)

    logger.info('create_market_buy_order')
    order = exchange.create_market_buy_order('NMR/USD', 0.01)

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
