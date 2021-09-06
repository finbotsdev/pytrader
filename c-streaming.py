# encoding: utf-8

import argparse
import config
import pytrader as pt
import pytrader.data as data
import pytrader.database as database
import pytrader.log as log
import pytrader.screener as screener
import pytrader.tradeapi as tradeapi
import threading


"""
    streaming
    ------


"""


timer = pt.Timer()

api = tradeapi.REST()

logger = log.logging
log.config_root_logger()


async def print_bar(bar):
    print('print_bar', bar)
    df = data.bars_dataframe([bars])
    print(df)

async def print_daily_bar(bar):
    print('print_daily_bar')
    df = data.bars_dataframe([bar])
    print(df)

async def print_quote(quote):
    print('print_quote', quote)
    df = data.quotes_dataframe([quote])
    print(df)

async def print_trade(trade):
    print('print_trade', trade)
    df = data.trades_dataframe([trade])
    print(df)

async def print_trade_update(tu):
    print('trade update', tu)

def main():
    stream = Stream(data_feed='iex', raw_data=True)

    symbols = ['AAPL','AMZN','GOOG','IBM','MSFT','TSLA']
    for symbol in symbols:
        stream.subscribe_bars(print_bar, symbol)
        stream.subscribe_daily_bars(print_daily_bar, symbol)
        stream.subscribe_quotes(print_quote, symbol)
        stream.subscribe_trades(print_trade, symbol)

    stream.subscribe_trade_updates(print_trade_update)

    @stream.on_bar("*")
    async def _(bar):
        print('on_bar', bar)
        pass

    @stream.on_status("*")
    async def _(status):
        print('on_status', status)
        pass

    stream.run()

if __name__ == "__main__":
    main()
