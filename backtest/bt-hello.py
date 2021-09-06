import backtrader as bt
import config
import pytrader as pt
from pytrader.backtest import argparse, data,
from pytrader.log import logger
import datetime
import os
import sys


"""
backtrader strategy - hello world
---------------------
a template for backtrader backtesting strategies

"""

class Strategy(bt.Strategy):

    def __init__(self):
        print("initializing strategy")
        self.data_ready = False

    def notify_data(self, data, status):
        print('Data Status =>', data._getstatusname(status))
        if status == data.LIVE:
            self.data_ready = True

    def log_data(self):
        ohlcv = []
        ohlcv.append(str(self.data.datetime.datetime()))
        ohlcv.append(str(self.data.open[0]))
        ohlcv.append(str(self.data.high[0]))
        ohlcv.append(str(self.data.low[0]))
        ohlcv.append(str(self.data.close[0]))
        ohlcv.append(str(self.data.volume[0]))
        print(",".join(ohlcv))

    def next(self):
        self.log_data()
        if not self.data_ready:
            return

def main(args):
    cerebro = bt.Cerebro()
    cerebro.broker.set_cash(1000000)
    cerebro.addstrategy(Strategy)
    cerebro.addsizer(bt.sizers.FixedSize, stake=1000)

    feed = data(source='yfinance', symbol=args.ticker, start=args.start, end=args.end)
    cerebro.adddata(feed)

    value = cerebro.broker.getvalue()
    print(f'Starting Portfolio Value ${value:,.2f}')

    cerebro.run()

    value = cerebro.broker.getvalue()
    print(f'Ending Portfolio Value ${value:,.2f}')

    cerebro.plot()

if __name__ == '__main__':
  args = argparse()
  print(args)

  timer = pt.Timer()
  logger.info(f'pytrader {__file__}')
  main(args)
  timer.report()
