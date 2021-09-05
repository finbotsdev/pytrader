import config
import sqlalchemy
from sqlalchemy import exc
from model import Session
from model.asset import Asset

"""
sqlalchemy5.py
-------------------------
asset uniquness

"""

session = Session()

try:
  a1 = Asset(
    company='AAA Holding',
    asset_class='us-equity',
    exchange='testexchange',
    status='test',
    symbol='AAA')

  a2 = Asset(
    company='AAA Holding',
    asset_class='us-equity',
    exchange='testexchange',
    status='test',
    symbol='AAA')

  session.add_all([a1, a2])

  print(a1)
  print(a2)

  session.commit()
except exc.SQLAlchemyError as e:
  print("######################## SQLALCHEMY ERROR")
  print("######################## SQLALCHEMY ERROR")
  print(e)
  print("######################## SQLALCHEMY ERROR")
  print("######################## SQLALCHEMY ERROR")
  pass
