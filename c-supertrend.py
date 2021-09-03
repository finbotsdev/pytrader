import ccxt
import pandas as pd
import schedule
import time


pd.set_option('display.max_rows', None)
pd.set_option('mode.chained_assignment', None)

exchange = ccxt.binanceus()

previous_bars = None

def TR(df):
  df['previous_close'] = df['close'].shift(1)
  df['high-low'] = df['high'] - df['low']
  df['high-pc'] = abs(df['high'] - df['previous_close'])
  df['low-pc'] = abs(df['low'] - df['previous_close'])
  df['TR'] = df[['high-low', 'high-pc', 'low-pc']].max(axis=1)
  df.drop(['previous_close', 'high-low', 'high-pc', 'low-pc'], axis=1, inplace=True)

def ATR(df):
  TR(df)
  df['ATR'] = df['TR'].rolling(14).mean()

def SuperTrend(df, period=7, multiplier=3):
  ATR(df)
  df['UB'] = ((df['high'] + df['low']) / 2) + (multiplier * df['ATR'])
  df['LB'] = ((df['high'] + df['low']) / 2) - (multiplier * df['ATR'])
  df['in_uptrend'] = True

  for current in range(1, len(df.index)):
    previous = current - 1
    prev_trend = df['in_uptrend'][previous]

    if df['close'][current] > df['UB'][previous]:
      df['in_uptrend'][current] = True
    elif df['close'][current] < df['LB'][previous]:
      df['in_uptrend'][current] = False
    else:
      df['in_uptrend'][current] = prev_trend

      if df['in_uptrend'][current] and df['LB'][current] < df['LB'][previous]:
        band = df['LB'][previous]
        df['LB'][current] = band

      if not df['in_uptrend'][current] and df['UB'][current] > df['UB'][previous]:
        band = df['UB'][previous]
        df['UB'][current] = band

def check_buy_sell_signal(df):
  last = len(df.index) - 1
  prev = last - 1

  # print(df.iloc[[-1]])
  # print(f"LAST: {df['timestamp'][last]} in_uptrend: {str(df['in_uptrend'][last])}")

  # print(df.iloc[[-2]])
  # print(f"PREV: {df['timestamp'][prev]} in_uptrend: {str(df['in_uptrend'][prev])}")

  if not isinstance(previous_bars, pd.DataFrame):
    print(f"starting in_uptrend: {str(df['in_uptrend'][last])}")
    return # first iteration

  else:
    lastlast = len(previous_bars.index) - 1
    if df['timestamp'][last] == previous_bars['timestamp'][lastlast]:
      return # no new data to evaluate

  print(f"{df['timestamp'][last]} {df['close'][last]} in_uptrend: {str(df['in_uptrend'][last])}")


  if not df['in_uptrend'][prev] and df['in_uptrend'][last]:
    print("!!!!!! BUY SIGNAL !!!!!!!!")

  if df['in_uptrend'][prev] and not df['in_uptrend'][last]:
    print("!!!!!! SELL SIGNAL !!!!!!!!")

def get_bars():
  bars = exchange.fetch_ohlcv('ETH/USDT', timeframe='1m', limit=30)
  df = pd.DataFrame(bars[:-1], columns=['timestamp','open','high','low','close','volume'])
  df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
  SuperTrend(df)
  return df

def execute_bot():
  global previous_bars
  current_bars = get_bars()
  check_buy_sell_signal(current_bars)
  previous_bars = current_bars


schedule.every(15).seconds.do(execute_bot)


while True:
  schedule.run_pending()
  time.sleep(1)
