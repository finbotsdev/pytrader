# encoding: utf-8

import pytrader as pt
from pytrader.data.cryptowatch import CryptowatchStream
from pytrader.log import logger
import traceback

"""
c-cryptowatch-stream.py
---------------------
pytrader function template
"""

def main(args):
  print(args)

  try:
    ws = CryptowatchStream()
    print(ws)
    ws.run()

  except Exception as e:
    logger.error(e)
    print(e)
    print(traceback.format_exc())


if __name__ == '__main__':
  parser = pt.ArgumentParser()
  parser.add_argument('-t', '--tickers', default=[], help="list of ticker symbols to include", nargs='+' )
  parser.add_argument("-v", "--verbose", action='store_true', help="verbose")
  args = parser.parse_args()

  timer = pt.Timer()
  logger.info(f'pytrader {__file__}')
  main(args)
  timer.report()
