import ccxt
import pandas as pd

# print a list of all available exchange classes
# print(ccxt.exchanges)

exchange = ccxt.coinbasepro()
bars = exchange.fetch_ohlcv('ETH/USDT', timeframe='1m', limit=30)
df = pd.DataFrame(bars, columns=['timestamp','open','high','low','close','volume'])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

print(df)
