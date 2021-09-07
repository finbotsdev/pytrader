# encoding: utf-8

from model import Session
from model.currency_pair import CurrencyPair
import pytrader as pt
from pytrader.data import Cryptowatch
from pytrader.log import logger
import traceback


"""
pairs.py
---------------------
sync digital asset records
"""


def main(args):
  print(args)

  try:
    logger.info('maintain crypto resources')

    session = Session()
    api = Cryptowatch()

    result = api.get_pairs()
    pairs = result['result']

    for p in pairs:
      pair = session.query(CurrencyPair).filter(
        CurrencyPair.symbol == p['symbol']).first()

      if not pair:
        logger.info(f"create record {p['symbol']}")
        pair = CurrencyPair(
          coinwatch_id=p['id'],
          base=p['base']['symbol'],
          quote=p['quote']['symbol'],
          symbol=p['symbol'])
        session.add(pair)
      else:
        logger.info(f"update record {p['symbol']}")
        pair.coinwatch_id=p['id']
        pair.base=p['base']['symbol']
        pair.quote=p['quote']['symbol']
        pair.symbol=p['symbol']

      session.commit()

    num_pairs = session.query(CurrencyPair).count()
    logger.info(f"{num_pairs} currency_pair records exist in the database")

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
