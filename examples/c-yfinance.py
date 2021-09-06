# encoding: utf-8

import pytrader as pt
from pytrader.data import YahooFinance
from pytrader.log import logger
import traceback


"""
c-yfinance.py
---------------------
fetch data from yfinance
"""


def main(args):
  print(args)

  try:
    logger.info('doing a thing')

    yf = YahooFinance()
    yf.set_symbol('AAPL')

    print(yf.actions())
    print(yf.balance_sheet())
    print(yf.calendar())
    print(yf.cashflow())
    print(yf.earnings())
    print(yf.dividends())
    print(yf.financials())
    print(yf.history(period = "1mo", interval = "1d"))
    print(yf.info())
    print(yf.isin())
    print(yf.institutional_holders())
    print(yf.major_holders())
    print(yf.options())
    print(yf.quarterly_balance_sheet())
    print(yf.quarterly_cashflow())
    print(yf.quarterly_earnings())
    print(yf.quarterly_financials())
    print(yf.recommendations())
    print(yf.sustainability())
    print(yf.ticker())

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
