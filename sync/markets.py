# encoding: utf-8

from model import Session
from model.market import Market
import pytrader as pt
from pytrader.data import Cryptowatch
from pytrader.log import logger
import traceback


"""
markets.py
---------------------
sync digital asset records
"""


def main(args):
  print(args)

  try:
    logger.info('maintain crypto resources')

    session = Session()
    api = Cryptowatch()

    result = api.get_markets()
    markets = result['result']

    for m in markets:
      print(m)
      market = session.query(Market).filter(
        Market.exchange == m['exchange'],
        Market.pair == m['pair']).first()

      if not market:
        logger.info(f"create record {m['id']} - {m['exchange']}")
        market = Market(
          coinwatch_id=m['id'],
          exchange=m['exchange'],
          pair=m['pair'],
          active=m['active'])
        session.add(market)
      else:
        logger.info(f"update record {m['id']} - {m['exchange']}")
        market.coinwatch_id=m['id']
        market.exchange=m['exchange']
        market.pair=m['pair']
        market.active=m['active']

      session.commit()

    num_markets = session.query(Market).count()
    logger.info(f"{num_markets} market records exist in the database")

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
