
import backtrader as bt
import config
import pytrader as pt
import datetime
import os
import sys

"""
backtrader strategy - opening breakout

"""

class Strategy(bt.Strategy):

    def __init__(self):
        print("initializing strategy")
        self.data_ready = False
        self.highest = bt.ind.Highest(self.data.high, period=5)
        self.lowest = bt.ind.Lowest(self.data.low, period=5)

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

        print("current highest high", self.highest[0])
        print("current lowest low", self.lowest[0])
        print("previous highest high", self.highest[-1])
        print("previous lowest low", self.lowest[-1])

        previous_highest_high = self.highest[-1]
        if self.data.close[0] > (previous_highest_high - 0.50):
            print(f"closed at {self.data.close[0]}, which is above previous high of {previous_highest_high}, let's buy!")
            # uncomment this if you want to buy
            # self.buy_bracket(limitprice=self.data.close[0]+1.00, price=self.data.close[0], stopprice=self.data.close[0]-0.50)

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
