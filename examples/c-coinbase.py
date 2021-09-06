# encoding: utf-8

import ccxt
import os
import pandas as pd
import pytrader as pt
from pytrader.data import AlpacaMarkets, date
import pytrader.log as log

timer = pt.Timer()

logger = log.logging
log.config_root_logger()

# print a list of all available exchange classes
# print(ccxt.exchanges)

exchange = ccxt.coinbasepro({
  'apiKey': os.environ.get('COINBASEPRO_API_KEY_ID'),
  'secret': os.environ.get('COINBASEPRO_API_SECRET_KEY'),
  'password': os.environ.get('COINBASEPRO_API_PASSWORD'),
  'TIMEOUT': 30000,
  'enableRateLimit': True
})

logger.info('exchange')
print(exchange)

logger.info('balances')
balances = exchange.fetch_balance()
print(f"ADA: {balances['total']['ADA']}")
print(f"USD: {balances['total']['USD']}")

logger.info('create_market_buy_order')
try:
  order = exchange.create_market_buy_order('NMR/USD', 0.01)
  print(order)
except Exception as e:
  print(e)

# markets = exchange.load_markets()
# for market in markets:
#   print(market)

# bars = exchange.fetch_ohlcv('ADA/USD', timeframe='1m', limit=30)
# df = pd.DataFrame(bars, columns=['timestamp','open','high','low','close','volume'])
# df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
# print(df)


timer.report()





