import config as cfg
from datetime import datetime
import pytrader as pt
from pytrader.data import AlpacaMarkets, date
from pytrader.log import logger
import sqlalchemy as sa
from sqlalchemy import exc

from model import Session
from model.asset import Asset
from model.price import Price


"""
c-sync-prices.py
---------------------
grab list of active tradable assets from database
for each active tradeable asset get historical minute data
"""


api = AlpacaMarkets()
session = Session()


def fetch_bars(symbol, end, start, timeframe='1Min', limit=5000):
  logger.debug(f'fetch_bars {symbol}: {type(symbol)} {end}: {type(end)} {start}: {type(start)}')
  result = api.get_bars(symbol, end=date(end), start=date(start), timeframe='1Min', limit=10000)
  if result and result['bars']:
    count = len(result['bars'])
    bars = result['bars']
  else:
    bars = []
  return bars

def fetch_range_bars(symbol, end, start):
  logger.debug(f'fetch_range_bars {symbol}: {type(symbol)} {end}: {type(end)} {start}: {type(start)}')
  # convert string dates to datetime objects
  dstart = datetime.strptime(date(start), '%Y-%m-%d')
  dend = datetime.strptime(date(end), '%Y-%m-%d')
  # get count of days between start and end date
  days_remaining = abs(dend-dstart).days

  # fetch bar data in week sized chunks
  bars = []
  while days_remaining > 0:
    start = days_remaining
    end = days_remaining -7
    days_remaining = days_remaining - 8

    start_date = date(f'{start} days ago')
    end_date = date(f'{end} days ago')

    res = fetch_bars(symbol, end_date, start_date)
    logger.info(f'{symbol} - {start_date} to {end_date} - {len(res)} bars returned')

    bars.extend(res)

  logger.info(f'{dstart} to {dend} - {len(bars)} minute bars')
  return bars

def main(args):
  logger.debug(args)

  try:
    logger.info('get assets list from local db')

    query = session.query(Asset).filter(
        Asset.status == 'active',
        Asset.is_tradeable == True)

    if args.tickers:
      query = query.filter(Asset.symbol.in_(args.tickers))

    assets = query.all()

    for asset in assets:
      bars = fetch_range_bars(asset.symbol, end=args.end, start=args.start)
      for b in bars:
        try:
          logger.info(f"create price for {asset.symbol} {b['t']} ")
          session.add(Price(
            asset_id=asset.id,
            period='minute',
            dt=b['t'],
            open=b['o'],
            high=b['h'],
            low=b['l'],
            close=b['c'],
            volume=b['v']
          ))
          session.commit()

        except Exception as e:
          session.rollback()
          logger.error(e)
          print(e)

    num_prices = session.query(Price).count()
    logger.info(f"{num_prices} price records exist in the database")

  except Exception as e:
    logger.error(e)
    print('asset', asset)
    print(e)
    print(traceback.format_exc())
    pass


if __name__ == '__main__':
  timer = pt.Timer()

  parser = pt.ArgumentParser()
  parser.add_argument("-e", "--end", default="yesterday", help="earliest date to include")
  parser.add_argument("-s", "--start", default="5 years ago", help="latest date to include")
  parser.add_argument('-t', '--tickers', default=[], help="list of ticker symbols to include", nargs='+' )
  parser.add_argument("-v", "--verbose", action='store_true', help="verbose")

  args = parser.parse_args()

  logger.info(f'pytrader {__file__}')

  main(args)

  timer.report()

# 252 trading days in years
# 6.5 hours in trading day
# 6.5 * 60 trading minutes in a day
# ~400 bars per day
# 2500 bars per week
# ~100k bars per year
