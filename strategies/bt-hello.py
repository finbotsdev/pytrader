import config as cfg
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
    logger.info('hello')

  except Exception as e:
    logger.error(e)
    pass


if __name__ == '__main__':
  parser = pt.ArgumentParser()
  parser.add_argument("-v", "--verbose", action='store_true', help="verbose")
  args = parser.parse_args()

  timer = pt.Timer()
  logger.info(f'pytrader {__file__}')
  main(args)
  timer.report()
