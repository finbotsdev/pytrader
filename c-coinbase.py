import ccxt
import pandas as pd

# print a list of all available exchange classes
# print(ccxt.exchanges)

exchange = ccxt.coinbasepro()
print(exchange)

markets = exchange.load_markets()

for market in markets:
  print(market)

# exchange_id = 'coinbasepro'
# exchange_class = getattr(ccxt, exchange_id)
# exchange = {
#   'apiKey' = 'YOUR_API_KEY'
#   'secret' = 'YOUR_SECRET'
#   'TIMEOUT' = 30000
#   'enableRateLimit' = True
# }

bars = exchange.fetch_ohlcv('ADA/USD', timeframe='1m', limit=30)
df = pd.DataFrame(bars, columns=['timestamp','open','high','low','close','volume'])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

print(df)
