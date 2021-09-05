import config as cfg
import pytrader as pt
from pytrader.data import AlpacaMarkets, date
from pytrader.log import logger
import sqlalchemy as sa
from sqlalchemy import exc

from model import Session
from model.asset import Asset
from model.price import Price


"""
c-sync-assets.py
---------------------
grab list of assets from data api and write to local database
for each active tradeable asset get yesterdays minute data
"""


api = AlpacaMarkets()
session = Session()


def main(args):
  print(args)

  try:
    logger.info('get assets list from exchange')
    assets = api.get_assets()

    for a in assets:
      asset = session.query(Asset).filter(
        Asset.symbol == a['symbol'],
        Asset.exchange == a['exchange']).first()

      if not asset:
        logger.info(f"create record {a['symbol']} - {a['name']}")
        asset = Asset(
          company=a['name'],
          asset_class=a['class'],
          exchange=a['exchange'],
          is_easy_to_borrow=a['easy_to_borrow'],
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
        asset.company=a['name']
        asset.asset_class=a['class']
        asset.exchange=a['exchange']
        asset.is_easy_to_borrow=a['easy_to_borrow']
        asset.is_fractionable=a['fractionable']
        asset.is_marginable=a['marginable']
        asset.is_shortable=a['shortable']
        asset.is_tradeable=a['tradable']
        asset.status=a['status']
        asset.symbol=a['symbol']

      session.commit()

    num_assets = session.query(Asset).count()
    logger.info(f"{num_assets} asset records exist in the database")

  except Exception as e:
    logger.error(e)
    print('a', a)
    print('asset', asset)
    print(e)
    pass


if __name__ == '__main__':
  timer = pt.Timer()

  parser = pt.ArgumentParser()
  parser.add_argument("-v", "--verbose", action='store_true', help="verbose")

  args = parser.parse_args()

  logger.info('pytrader initializing')

  main(args)

  timer.report()
