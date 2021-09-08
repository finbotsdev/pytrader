# encoding: utf-8

import pytrader as pt
from pytrader.data import IEXCloud
from pytrader.log import logger
import traceback


"""
c-hello.py
---------------------
pytrader function template
"""


def main(args):
  print(args)

  try:
    logger.info('get data from iex api')

    api = IEXCloud()

    api.set_symbol('MSFT')

    logger.info('get_logo')
    print(api.get_logo())

    logger.info('get_company_info')
    print(api.get_company_info())

    logger.info('get_company_news')
    print(api.get_company_news())

    logger.info('get_stats')
    print(api.get_stats())

    logger.info('get_fundamentals')
    print(api.get_fundamentals())

    logger.info('get_dividends')
    print(api.get_dividends())

    logger.info('get_institutional_ownership')
    print(api.get_institutional_ownership())

    logger.info('get_insider_transactions')
    print(api.get_insider_transactions())

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
