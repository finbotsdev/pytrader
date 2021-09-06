# encoding: utf-8

import config
import sqlalchemy
from sqlalchemy import exc
from model import Session
from model.asset import Asset
from model.price import Price

"""
sqlalchemy3.py
-------------------------
working with related models

"""

session = Session()

try:

  asset = Asset(
    company='mycompany',
    asset_class='us-equity',
    exchange='NYSE',
    status='test',
    symbol='QIK')
  session.add(asset)
  session.commit()

  print('asset')
  print(asset)

  prices = [
    Price(asset_id=asset.id, period='minute', dt='2021-09-03 13:30:00', open=1.01, high=2.30, low=0.90, close=2.01, volume=13241234),
    Price(asset_id=asset.id, period='minute', dt='2021-09-03 13:31:00', open=2.01, high=3.90, low=1.90, close=2.80, volume=12344412)
  ]
  session.add_all(prices)
  session.commit()

  print('asset prices')
  print(asset.prices)

except exc.SQLAlchemyError as e:
  print("######################## SQLALCHEMY ERROR")
  print("######################## SQLALCHEMY ERROR")
  print(e)
  print("######################## SQLALCHEMY ERROR")
  print("######################## SQLALCHEMY ERROR")
  pass
