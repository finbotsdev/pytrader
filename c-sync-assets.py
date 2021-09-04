import config as cfg
import psycopg2 as pg
import psycopg2.extras as pgx
import pytrader as pt
from pytrader.data import AlpacaMarkets, date
import pytrader.log as log

"""
c-sync-aqssets.py
---------------------
grab list of assets from data api and write to local database
for each active tradeable asset get yesterdays minute data
"""

timer = pt.Timer()

logger = log.logging
log.config_root_logger()

conn = pg.connect(dsn=cfg.DSN, cursor_factory=pgx.DictCursor)
cursor = conn.cursor()

api = AlpacaMarkets()

logger.info('get assets list from exchange')
assets = api.get_assets()

for a in assets:
    cursor.execute("""
      SELECT id
      FROM asset
      WHERE symbol = %s
      AND exchange = %s
    """, (a['symbol'], a['exchange']))
    asset = cursor.fetchone()

    if asset:
      logger.info(f"update record for {a['name']} ({a['symbol']})")
      cursor.execute("""
        UPDATE asset
        SET
          company = %s,
          asset_class = %s,
          exchange = %s,
          is_easy_to_borrow = %s,
          is_fractionable = %s,
          is_marginable = %s,
          is_shortable = %s,
          is_tradeable = %s,
          status = %s,
          symbol = %s
        WHERE id = %s
      """, (a['name'], a['class'], a['exchange'], a['easy_to_borrow'], a['fractionable'], a['marginable'], a['shortable'], a['tradable'], a['status'], a['symbol'], asset['id']))
    else:
      logger.info(f"create record for {a['name']} ({a['symbol']})")
      cursor.execute("""
          INSERT INTO asset (company, asset_class, exchange, is_easy_to_borrow, is_fractionable, is_marginable, is_shortable, is_tradeable, status, symbol)
          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
      """, (a['name'], a['class'], a['exchange'], a['easy_to_borrow'], a['fractionable'], a['marginable'], a['shortable'], a['tradable'], a['status'], a['symbol'],))
    conn.commit()

    cursor.execute("""
      SELECT id
      FROM asset
      WHERE symbol = %s
      AND exchange = %s
    """, (a['symbol'], a['exchange']))
    asset = cursor.fetchone()

    if a['status']=='active' and a['tradable']:
      result = api.get_bars(a['symbol'], end=date('yesterday'), start=date('yesterday'), timeframe='1Min')
      bars = result['bars']
      if bars:
        for b in bars:
          try:
            cursor.execute("""
                INSERT INTO price (asset_id, dt, period, open, high, low, close, volume)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (asset['id'], b['t'], 'minute', b['o'], b['h'], b['l'], b['c'], b['v'],))
            conn.commit()
          except Exception as e:
            logger.error(e)
            conn.rollback()
            print(e)


cursor.execute("""
  SELECT * FROM asset
""")
assets = cursor.fetchall()
logger.info(f"{len(assets)} asset records exist in the database")

cursor.execute("""
  SELECT * FROM price
""")
prices = cursor.fetchall()
logger.info(f"{len(prices)} price records exist in the database")

timer.report()
