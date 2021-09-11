# encoding: utf-8

import pytrader as pt
from pytrader.data import CoinbaseProStream
from pytrader.log import logger
import traceback


"""
coinbasepro.py
---------------------
stream data from coinbasepro websocket
"""


def main(args):
  try:
    logger.info('pytrader coinbasepro stream')
    logger.debug(args)

    ws = CoinbaseProStream()
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
