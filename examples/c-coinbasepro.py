# encoding: utf-8

import pytrader as pt
from pytrader.data import CoinbasePro
from pytrader.log import logger
import traceback


"""
c-coinbasepro.py
---------------------
pytrader function template
"""


def main(args):
  print(args)

  try:
    logger.info('get data from coinbase pro api')

    api = CoinbasePro()

    logger.info('get_time')
    print(api.get_time())

    logger.info('get_accounts')
    print(api.get_accounts())


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
