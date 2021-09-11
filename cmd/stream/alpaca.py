# encoding: utf-8

import pytrader as pt
from pytrader.data import AlpacaStream
from pytrader.log import logger
import traceback


"""
alpaca.py
---------------------
stream data from alpaca websocket
"""


def main(args):
  try:
    logger.info('pytrader alpaca stream')
    logger.debug(args)

    ws = AlpacaStream()
    ws.set_tickers(args.tickers)
    ws.run()

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
