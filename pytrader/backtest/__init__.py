# encoding: utf-8

import backtrader as bt
import os
import pandas as pd
import pytrader as pt
from pytrader.database import Session
from pytrader.date import date
from pytrader.model import Asset, Ohlcv
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

def feed(source: str, symbol: str, start: str ='one year ago', end: str = 'yesterday', interval: str = 'day'):
  """
  feed
  ----------------------

  """

  fds, dt_start = date(start)
  tds, dt_end = date(end)

  if source == 'csvfile':
    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    datapath = os.path.join(modpath, '../', '.data', interval, f'{symbol}.csv')

    if interval == 'day':
      return bt.feeds.YahooFinanceCSVData(
        dataname=datapath,
        fromdate=dt_start,
        todate=dt_end,
        reverse=False)

    if interval == 'minute':

      df = pd.DataFrame()
      df = pd.read_csv(datapath)
      df['dt'] = pd.to_datetime(df['dt'])
      df.set_axis(['datetime', 'open', 'high', 'low', 'close', 'volume'], axis=1, inplace=True)
      return bt.feeds.PandasData(
        dataname=df,
        datetime='datetime',
        high=2,
        low=3,
        open=1,
        close=4,
        volume=5,
      )

  if source == 'database':
    asset = session.query(Asset.id).filter(
      Asset.symbol == symbol).first()

    prices = session.query(
      Ohlcv.dt.label('dt'),
      Ohlcv.open.label('open'),
      Ohlcv.high.label('high'),
      Ohlcv.low.label('low'),
      Ohlcv.close.label('close'),
      Ohlcv.volume.label('volume')
    ).filter(
      Ohlcv.asset_id == asset.id,
      Ohlcv.dt >= dt_start,
      Ohlcv.dt <= dt_end,
      text("ohlcv.dt::time >= make_time(9, 30, 0) "),
      text("ohlcv.dt::time <= make_time(16, 0, 0)")
    ).order_by(Ohlcv.dt.asc()).all()
    print(prices)

    df = pd.DataFrame(prices)
    df.set_axis(['datetime', 'open', 'high', 'low', 'close', 'volume'], axis=1, inplace=True)

    return bt.feeds.PandasData(dataname=df, datetime='datetime')
