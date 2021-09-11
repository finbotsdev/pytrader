
from pytrader.data import AlpacaMarkets
from pytrader.database import Session
from pytrader.log import logger
from pytrader.model import Asset, Ohlcv


"""
  bars
  ------
  fetch ohlcv data from alapaca and write to database

"""


def argparser(subparser):
  parser = subparser.add_parser('bars')
  parser.add_argument("-e", "--end", default="yesterday", help="earliest date to include")
  parser.add_argument("-s", "--start", default="5 years ago", help="latest date to include")
  parser.add_argument('-t', '--tickers', default=[], help="list of ticker symbols to include", nargs='+' )


def main(args):
  logger.debug('pytrader history')
  logger.debug(args)

  session = Session()

  api = AlpacaMarkets()

  logger.info('get assets list from local db')
  query = session.query(Asset).filter(
    Asset.status == 'active',
    Asset.is_tradeable == True)

  if args.tickers:
    query = query.filter(Asset.symbol.in_(args.tickers))

  assets = query.all()

  for asset in assets:
    bars = api.get_bars_chunked(asset.symbol, end=args.end, start=args.start)
    for b in bars:
      try:
        logger.info(f"create ohlcv for {asset.symbol} {b['t']} ")
        session.add(Ohlcv(
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

  num_prices = session.query(Ohlcv).count()
  logger.info(f"{num_prices} ohlcv records exist in the database")
