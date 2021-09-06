import pytrader as pt
from pytrader.data import Cryptowatch
from pytrader.log import logger


"""
c-cryptowatch.py
---------------------
fetch data from cryptowatch api
"""

def main(args):
  print(args)

  try:
    api = Cryptowatch()

    logger.info('get_assets')
    print(api.get_assets())

    logger.info('get_asset')
    print(api.get_asset('btc'))

    logger.info('get_pairs')
    print(api.get_pairs())

    logger.info('get_pair')
    print(api.get_pair('btcusd'))

    logger.info('get_exchanges')
    print(api.get_exchanges())

    logger.info('get_exchange')
    print(api.get_exchange('bittrex'))

    logger.info('get_exchange_markets')
    print(api.get_exchange_markets('bittrex'))

    logger.info('get_markets')
    print(api.get_markets())

    logger.info('get_market')
    print(api.get_market('bittrex', 'btcusd'))

    logger.info('get_market_price')
    print(api.get_market_price('bittrex', 'btcusd'))

    logger.info('get_market_trades')
    print(api.get_market_trades('bittrex', 'btcusd'))

    logger.info('get_market_summary')
    print(api.get_market_summary('bittrex', 'btcusd'))

    logger.info('get_market_orderbook')
    print(api.get_market_orderbook('bittrex', 'btcusd'))

    logger.info('get_market_ohlc')
    print(api.get_market_ohlc('bittrex', 'btcusd'))

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
