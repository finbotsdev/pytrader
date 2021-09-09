# encoding: utf-8

import pytrader as pt
from pytrader.data import AlpacaMarkets, CoinbasePro
from pytrader.database import Session
from pytrader.log import logger
from pytrader.model import Asset, Exchange
import traceback


"""
stock.py
---------------------
sync asset records
"""


def main(args):
  print(args)

  try:
    session = Session()

    api = AlpacaMarkets()
    assets = api.get_assets()

    for a in assets:
      symbol = api.exchange_map(a['exchange'])

      exchange = session.query(Exchange).filter(
        Exchange.symbol == symbol).first()

      asset = session.query(Asset).filter(
        Asset.symbol == a['symbol'],
        Asset.exchange_id == exchange.id).first()

      if not asset:
        logger.info(f"create record {a['symbol']} - {a['name']}")
        asset = Asset(
          name=a['name'],
          asset_class=a['class'],
          exchange_id=exchange.id,
          is_etf=False,
          is_fractionable=a['fractionable'],
          is_marginable=a['marginable'],
          is_shortable=a['shortable'],
          is_tradeable=a['tradable'],
          status=a['status'],
          symbol=a['symbol'])
        session.add(asset)
      else:
        logger.info(f"update record {a['symbol']} - {a['name']}")
        asset.name=a['name']
        asset.asset_class=a['class']
        asset.exchange_id=exchange.id
        asset.is_fractionable=a['fractionable']
        asset.is_marginable=a['marginable']
        asset.is_shortable=a['shortable']
        asset.is_tradeable=a['tradable']
        asset.status=a['status']
        asset.symbol=a['symbol']

      session.commit()


    api = CoinbasePro()
    assets = api.get_products()
    for asset in assets:
      print(asset)

    for a in assets:
      exchange = session.query(Exchange).filter(
        Exchange.symbol == 'coinbase-pro').first()

      asset = session.query(Asset).filter(
        Asset.symbol == a['id'],
        Asset.exchange_id == exchange.id).first()

      if not asset:
        logger.info(f"create record {a['id']} - {a['display_name']}")
        asset = Asset(
          name=a['display_name'],
          asset_class='digital',
          exchange_id=exchange.id,
          status=a['status'],
          symbol=a['id'])
        session.add(asset)
      else:
        logger.info(f"update record {a['id']} - {a['display_name']}")
        asset.name=a['display_name']
        asset.asset_class='digital'
        asset.exchange_id=exchange.id
        asset.status=a['status']
        asset.symbol=a['id']

      session.commit()

    num_assets = session.query(Asset).count()
    logger.info(f"{num_assets} asset records exist in the database")

  except Exception as e:
    logger.error(e)
    print(e)
    print(traceback.format_exc())


if __name__ == '__main__':
  parser = pt.ArgumentParser()
  parser.add_argument("-v", "--verbose", action='store_true', help="verbose")
  args = parser.parse_args()

  timer = pt.Timer()
  logger.info(f'pytrader {__file__}')
  main(args)
  timer.report()
