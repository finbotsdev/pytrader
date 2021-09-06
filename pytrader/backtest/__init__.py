import backtrader as bt
from datetime import datetime

import os
import pytrader as pt
from pytrader.data import date
import sys


def argparse():
  parser = pt.ArgumentParser()
  parser.add_argument("-v", "--verbose", action='store_true', help="verbose")
  parser.add_argument("-e", "--end", default="yesterday", help="earliest date to include")
  parser.add_argument("-i", "--interval", default="day", help="market data aggregation level (day or minute)")
  parser.add_argument("-s", "--start", default="5 years ago", help="latest date to include")
  parser.add_argument('-t', '--ticker', default='AAPL', help="ticker symbol to include" )
  return parser.parse_args()


def data(source: str, symbol: str, start: str ='one year ago', end: str = 'yesterday'):
  modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
  datapath = os.path.join(modpath, '../', '.data', 'day', f'{symbol}.csv')

  fds, fromdate = date(start)
  tds, todate = date(end)

  return bt.feeds.YahooFinanceCSVData(
      dataname=datapath,
      fromdate=fromdate,
      todate=todate,
      reverse=False)

