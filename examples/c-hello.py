# encoding: utf-8

import pytrader as pt
from pytrader.log import logger


"""
c-hello.py
---------------------
pytrader function template
"""


def main(args):
  print(args)

  try:
    logger.info('doing a thing')

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
