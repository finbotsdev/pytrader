import config
import sqlalchemy
from sqlalchemy import exc
from model import Session
from model.asset import Asset
from model.etf_holding import EtfHolding

"""
sqlalchemy4.py
-------------------------
working with complex related models

NOTE:
how to define within the constraints of sqlalchemy
the pseudo polymorphic relationship between an asset which is an etf
and an asset which is a holding of an etf is complicated

for now we will manage these relaitonships manually
"""

session = Session()

try:
  etf = Asset(
    company='AAA ETF',
    asset_class='us-equity',
    exchange='testexchange',
    status='test',
    symbol='AAA1')

  holding = Asset(
    company='AAA Holding',
    asset_class='us-equity',
    exchange='testexchange',
    status='test',
    symbol='AAA2')

  etf.holdings = [holding]

  session.add_all([etf, holding])

  print('etf')
  print(etf)
  print(etf.holdings)

  # print('holding')
  # print(holding)

  session.commit()
except exc.SQLAlchemyError as e:
  print("######################## SQLALCHEMY ERROR")
  print("######################## SQLALCHEMY ERROR")
  print(e)
  print("######################## SQLALCHEMY ERROR")
  print("######################## SQLALCHEMY ERROR")
  pass
