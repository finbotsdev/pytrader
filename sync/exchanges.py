# encoding: utf-8

from model import Session
from model.exchange import Exchange
import pytrader as pt
from pytrader.data import Cryptowatch
from pytrader.log import logger
import traceback


"""
exchanges.py
---------------------
sync digital asset records
"""


def main(args):
  print(args)

  try:
    session = Session()
    api = Cryptowatch()

    result = api.get_exchanges()
    exchanges = result['result']

    for e in exchanges:
      exchange = session.query(Exchange).filter(
        Exchange.symbol == e['symbol']).first()

      if not exchange:
        logger.info(f"create record {e['symbol']} - {e['name']}")
        exchange = Exchange(
          coinwatch_id=e['id'],
          name=e['name'],
          symbol=e['symbol'],
          active=e['active'])
        session.add(exchange)
      else:
        logger.info(f"update record {e['symbol']} - {e['name']}")
        exchange.coinwatch_id=e['id']
        exchange.name=e['name']
        exchange.symbol=e['symbol']
        exchange.symbol=e['symbol']

      session.commit()

    num_exchanges = session.query(Exchange).count()
    logger.info(f"{num_exchanges} exchange records exist in the database")

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
