# encoding: utf-8

from model import Session
from model.digital_asset import DigitalAsset
import pytrader as pt
from pytrader.log import logger
import traceback


"""
crypto.py
---------------------
sync digital asset records
"""


def main(args):
  print(args)

  try:
    logger.info('maintain crypto resources')


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
