# encoding: utf-8

import backtrader as bt
import os
from model import Session
from model.asset import Asset
from model.price import Price
import pandas as pd
import pytrader as pt
from pytrader.data import date
from sqlalchemy.sql import text
import sys

session = Session()

def cli_options_parser():
  parser = pt.ArgumentParser()
  parser.add_argument("-v", "--verbose", action='store_true', help="verbose")
  parser.add_argument("-e", "--end", default="yesterday", help="earliest date to include")
  parser.add_argument("-i", "--interval", default="day", help="market data aggregation level (day or minute)")
  parser.add_argument("-s", "--start", default="5 years ago", help="latest date to include")
  parser.add_argument('-t', '--ticker', default='AAPL', help="ticker symbol to include" )
  return parser.parse_args()

def feed(source: str, symbol: str, start: str ='one year ago', end: str = 'yesterday'):
  """
  feed
  ----------------------

  """
  modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
  datapath = os.path.join(modpath, '../', '.data', 'day', f'{symbol}.csv')

  fds, dt_start = date(start)
  tds, dt_end = date(end)

  if source == 'yfinance':
    return bt.feeds.YahooFinanceCSVData(
      dataname=datapath, fromdate=dt_start,
      todate=dt_end, reverse=False)

  if source == 'local':
    asset = session.query(Asset.id).filter(
      Asset.symbol == symbol).first()

    prices = session.query(
      Price.dt.label('dt'),
      Price.open.label('open'),
      Price.high.label('high'),
      Price.low.label('low'),
      Price.close.label('close'),
      Price.volume.label('volume')
    ).filter(
      Price.asset_id == asset.id,
      Price.dt >= dt_start,
      Price.dt <= dt_end,
      text("price.dt::time >= make_time(9, 30, 0) "),
      text("price.dt::time <= make_time(16, 0, 0)")
    ).order_by(Price.dt.asc()).all()

    df = pd.DataFrame(prices)
    df.set_axis(['datetime', 'open', 'high', 'low', 'close', 'volume'], axis=1, inplace=True)

    return bt.feeds.PandasData(dataname=df, datetime='datetime')
