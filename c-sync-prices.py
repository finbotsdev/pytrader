import config as cfg
import pytrader as pt
from pytrader.data import AlpacaMarkets, date
import pytrader.log as log
import sqlalchemy as sa
from sqlalchemy import exc

from model import Session
from model.asset import Asset
from model.price import Price

"""
c-sync-aqssets.py
---------------------
grab list of assets from data api and write to local database
for each active tradeable asset get yesterdays minute data
"""

timer = pt.Timer()

logger = log.logging
log.config_root_logger()

api = AlpacaMarkets()
session = Session()

try:
  logger.info('get assets list from local db')
  assets = api.get_assets()
  assets = session.query(Asset).filter(
    Asset.status == 'active',
    Asset.is_tradeable == True).all()

  for asset in assets:
    print()
    print(asset)

    result = api.get_bars(asset.symbol, end=date('yesterday'), start=date('yesterday'), timeframe='1Min')
    bars = result['bars']
    if bars:
      for b in bars:
        try:
          logger.info(f"create price for {asset.symbol} {b['t']} ")
          price = Price(
            asset_id=asset.id,
            period='minute',
            dt=b['t'],
            open=b['o'],
            high=b['h'],
            low=b['l'],
            close=b['c'],
            volume=b['v']
          )
          session.add(price)
          session.commit()

        except Exception as e:
          session.rollback()
          logger.error(e)
          print(e)

  num_prices = session.query(Price).count()
  logger.info(f"{num_prices} price records exist in the database")

except Exception as e:
  logger.error(e)
  print('asset', asset)
  print(e)
  pass

timer.report()
