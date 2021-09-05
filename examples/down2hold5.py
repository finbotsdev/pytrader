import backtrader as bt
import config
import pytrader as pt
import datetime
import os
import sys


"""
backtrader strategy - hold5

if closing price is down for two consecutive periods buy
sell position after 5 periods
"""


class Strategy(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print(f'{dt.isoformat()}, {txt}')

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        self.order = None

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log(f'Close, {self.dataclose[0]:.2f}')

        if not self.position:
            if self.dataclose[0] < self.dataclose[-1]:
                # current close is less than previous close
                if self.dataclose[-1] < self.dataclose[-2]:
                    # previous close less than previous close
                    self.log(f'BUY, {self.dataclose[0]:.2f}')
                    self.buy()

        else:
            if len(self) >= (self.bar_executed + 5):
                # sell our position after 5 periods
                self.log(f'SELL, {self.dataclose[0]:.2f}')
                self.sell()

    def notify(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status == order.Completed:
            if order.isbuy():
                self.log(f'BUY EXECUTED, {order.executed.price:.2f}')

            elif order.issell():
                self.log(f'SELL EXECUTED, {order.executed.price:.2f}')

            self.bar_executed = len(self)


def data(t):
    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    datapath = os.path.join(modpath, '.data', 'day', f'{t}.csv')

    # data = bt.feeds.YahooFinanceCSVData(
    #     dataname=datapath,
    #     fromdate=datetime.datetime(2020,1,1),
    #     todate=datetime.datetime(2020,12,31),
    #     reverse=False)

    # generic csv data to match our alapca downloads

    data = bt.feeds.GenericCSVData(
        dataname=datapath,
        fromdate=datetime.datetime(2016, 1, 1),
        todate=datetime.datetime(2020, 12, 31),

        nullvalue=0.0,

        dtformat=('%Y-%m-%d %H:%M:%S'),
        datetime=0,
        high=2,
        low=3,
        open=5,
        close=1,
        volume=6,
        openinterest=-1
    )

    # store = bt.stores.IBStore(port=7497)
    # data = store.getdata(dataname='AAPL', sectype='STK', exchange='ISLAND', timeframe=bt.TimeFrame.Minutes)
    return data

def main(args):
    cerebro = bt.Cerebro()
    cerebro.broker.set_cash(1000000)
    cerebro.addstrategy(Strategy)
    cerebro.addsizer(bt.sizers.FixedSize, stake=1000)
    cerebro.adddata(data(args.ticker))

    value = cerebro.broker.getvalue()
    print(f'Starting Portfolio Value ${value:,.2f}')

    cerebro.run()

    value = cerebro.broker.getvalue()
    print(f'Ending Portfolio Value ${value:,.2f}')

    cerebro.plot()

if __name__ == '__main__':
    parser = pt.ArgumentParser()
    parser.add_argument("-v", "--verbose", action='store_true', help="verbose")
    parser.add_argument('-s', '--strategy', default='openbreakout', help="the strategy" )
    parser.add_argument('-t', '--ticker', default='AAPL', help="the ticker symbol" )
    args = parser.parse_args()

    main(args)
