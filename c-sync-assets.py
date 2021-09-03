import config as cfg
import psycopg2 as pg
import psycopg2.extras as pgx
from pytrader.data import AlpacaMarkets

"""
c-sync-aqssets.py
---------------------
grab list of assets from data api and write to local database

TODO:
    upsert
"""

connection = pg.connect(dsn=cfg.DSN, cursor_factory=pgx.DictCursor)
cursor = connection.cursor()

api = AlpacaMarkets()

assets = api.get_assets()

for a in assets:
    print(a)
    cursor.execute("""
        INSERT INTO stocks (company, asset_class, exchange, is_easy_to_borrow, is_fractionable, is_marginable, is_shortable, is_tradeable, status, symbol)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (a['name'], a['class'], a['exchange'], a['easy_to_borrow'], a['fractionable'], a['marginable'], a['shortable'], a['tradable'], a['status'], a['symbol'],))

connection.commit()

cursor.execute('SELECT * FROM stocks')

stocks = cursor.fetchall()

for stock in stocks:
    print(stock['symbol'])
