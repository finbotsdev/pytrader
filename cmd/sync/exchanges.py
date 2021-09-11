# encoding: utf-8

import pytrader as pt
from pytrader.data import IEXCloud, Cryptowatch
from pytrader.database import Session
from pytrader.log import logger
from pytrader.model import Exchange
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

    api = IEXCloud()
    exchanges = api.get_exchanges_us()
    for e in exchanges:
      exchange = session.query(Exchange).filter(
        Exchange.symbol == e['mic']).first()

      if not exchange:
        logger.info(f"create record {e['mic']} - {e['name']} - {e['type']}")
        exchange = Exchange(
          name=e['name'],
          symbol=e['mic'],
          exchange_class=e['type'],
          active=True)
        session.add(exchange)
      else:
        logger.info(f"update record {e['mic']} - {e['name']} - {e['type']}")
        exchange.name=e['name']
        exchange.symbol=e['mic']
        exchange.exchange_class=e['type']

    session.commit()

    cwapi = Cryptowatch()
    result = cwapi.get_exchanges()
    exchanges = result['result']

    for e in exchanges:
      exchange = session.query(Exchange).filter(
        Exchange.symbol == e['symbol']).first()

      if not exchange:
        logger.info(f"create record {e['symbol']} - {e['name']}")
        exchange = Exchange(
          name=e['name'],
          symbol=e['symbol'],
          active=e['active'],
          exchange_class='digital')
        session.add(exchange)
      else:
        logger.info(f"update record {e['symbol']} - {e['name']}")
        exchange.name=e['name']
        exchange.symbol=e['symbol']
        exchange.active=e['active']
        exchange.exchange_class='digital'

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
