# encoding: utf-8

from model import Session
from model.digital_asset import DigitalAsset
import pytrader as pt
from pytrader.data import Cryptowatch
from pytrader.log import logger
import traceback


"""
crypto.py
---------------------
sync digital asset records
"""


def main(args):
  print(args)

  try:
    logger.info('maintain crypto resources')

    session = Session()
    api = Cryptowatch()

    result = api.get_assets()
    assets = result['result']

    for a in assets:
      asset = session.query(DigitalAsset).filter(
        DigitalAsset.symbol == a['symbol']).first()

      if not asset:
        logger.info(f"create record {a['symbol']} - {a['name']}")
        asset = DigitalAsset(
          coinwatch_id=a['id'],
          name=a['name'],
          symbol=a['symbol'])
        session.add(asset)
      else:
        logger.info(f"update record {a['symbol']} - {a['name']}")
        asset.coinwatch_id=a['id']
        asset.name=a['name']
        asset.symbol=a['symbol']

      session.commit()

    num_assets = session.query(DigitalAsset).count()
    logger.info(f"{num_assets} digitalasset records exist in the database")

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
