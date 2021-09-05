import config as cfg
from crontab import CronTab
import pytrader as pt
from pytrader.log import logger


"""
c-sync-crontab.py
---------------------
manage cron tasks
"""


def main(args):
  pass

if __name__ == '__main__':
  timer = pt.Timer()

  parser = pt.ArgumentParser()
  parser.add_argument("-v", "--verbose", action='store_true', help="verbose")

  args = parser.parse_args()

  logger.info('pytrader initializing')

  main(args)

  timer.report()
