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


updated = {}


def update(symbol, bars):
  global updated

  datadir = f'./.data/minute'
  datafile = f'.data/minute/{symbol}.csv'

  # ignore the first update as it may not
  # be a complete minute bar
  if symbol not in updated.keys():
    updated[symbol] = bars
    return

  out = open(datafile, "a")
  for timestamp in bars:
    ohclv = bars[timestamp]
    print(symbol, timestamp, ohclv)
    out.write(f"{timestamp},{ohclv['open']},{ohclv['high']},{ohclv['low']},{ohclv['close']},{ohclv['volume']}\n")
    out.close()

def main(args):
  try:
    logger.info('pytrader coinbasepro stream')
    logger.debug(args)

    ws = CoinbaseProStream()
    ws.set_on_update(update)
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
