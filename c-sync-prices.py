import config as cfg
import psycopg2 as pg
import psycopg2.extras as pgx
import pandas as pd
import pytrader as pt
from pytrader.data import AlpacaMarkets, date
import pytrader.log as log

timer = pt.Timer()

logger = log.logging
log.config_root_logger()

api = AlpacaMarkets()
conn = pg.connect(dsn=cfg.DSN, cursor_factory=pgx.DictCursor)
cursor = conn.cursor()

symbol = 'AAPL'
period = '1Min'

result = api.get_bars(symbol, end=date('yesterday'), start=date('yesterday'), timeframe=period)
logger.info(result)

cursor.execute("""
  SELECT * FROM asset WHERE symbol = %s AND status = 'active' AND is_tradeable = true
""", (symbol,))
asset = cursor.fetchone()
logger.info(asset)

bars = result['bars']
for b in bars:
  # logger.info(b)
  cursor.execute("""
      INSERT INTO prices (asset_id, dt, period, open, high, low, close, volume)
      VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
  """, (asset['id'], b['t'], 'minute', b['o'], b['h'], b['l'], b['c'], b['v'],))

conn.commit()

timer.report()

# 2021-09-04 09:52:25,352| MainThread | INFO | 12310 asset records exist in the database
# 2021-09-04 09:52:39,813| MainThread | INFO | 1437744 price records exist in the database
# 2021-09-04 09:52:39,813| MainThread | INFO | --- 9768.414362192154 seconds ---
