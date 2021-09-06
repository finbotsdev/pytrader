# encoding: utf-8

import config
import sqlalchemy
from model import Session
from model.asset import Asset
from model.etf_holding import EtfHolding
from model.price import Price
from model.mention import Mention

"""
sqlalchemy2.py
-------------------------
learning basic querying and filtering of records

"""

session = Session()

# In the case where your application does not yet have an Engine when you define your module-level objects, just set it up like this:
# Session = sessionmaker()
# Later, when you create your engine with create_engine(), connect it to the Session using sessionmaker.configure():
# Session.configure(bind=engine)  # once engine is available

# query records from database

# SELECT
#   asset.id AS asset_id,
#   asset.company AS asset_company,
#   asset.asset_class AS asset_asset_class,
#   asset.exchange AS asset_exchange,
#   asset.is_easy_to_borrow AS asset_is_easy_to_borrow,
#   asset.is_etf AS asset_is_etf,
#   asset.is_fractionable AS asset_is_fractionable,
#   asset.is_marginable AS asset_is_marginable,
#   asset.is_shortable AS asset_is_shortable,
#   asset.is_tradeable AS asset_is_tradeable,
#   asset.status AS asset_status,
#   asset.symbol AS asset_symbol
# FROM asset
# query = session.query(Asset)
# print(query)

# SELECT
#   asset.symbol AS asset_symbol,
#   asset.company AS asset_company
# FROM asset
# query = session.query(Asset.symbol, Asset.company)
# print(query)

# SELECT
#   asset.id AS asset_id,
#   asset.company AS whodat
# FROM asset
# query = session.query(Asset.id, Asset.company.label('whodat'))
# print(query)

# FROM asset
# ORDER BY asset.symbol
# LIMIT %(param_1)s
# OFFSET %(param_2)s
# query = session.query(Asset.symbol, Asset.company)
# query = query.order_by(Asset.symbol)[1:3]
# print(query)

# SELECT
#   asset.symbol AS asset_symbol,
#   asset.company AS asset_company
# FROM asset
# WHERE asset.symbol = %(symbol_1)s
# query = session.query(Asset.symbol, Asset.company)
# query = query.filter_by(symbol='AAPL')
# print(query)

# SELECT
#   asset.symbol AS asset_symbol,
#   asset.company AS asset_company
# FROM asset
# WHERE asset.company LIKE %(company_1)s
# AND asset.symbol IN ([POSTCOMPILE_symbol_1])
query = session.query(Asset.symbol, Asset.company)
query = query.filter(Asset.company.like('%ETF%'))
print(f'{query.count()} records are notes as ETF')


query = query.filter(Asset.symbol.in_(['ARKF', 'ARKG', 'ARKK', 'ARKQ', 'ARKX']))
for asset in query:
  print(asset.symbol, asset.company)

