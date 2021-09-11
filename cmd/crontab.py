# -*- coding: utf-8 -*-

from crontab import CronTab
import getpass
import os
from pytrader.log import logger


"""
  crontab
  ------
  update crontab for pytrader
"""


def argparser(subparser):
  parser = subparser.add_parser('crontab')


def main(args):
  logger.debug('pytrader crontab')
  logger.debug(args)

  current_user = getpass.getuser()
  cwd = os.getcwd()
  cron = CronTab(user=current_user)

  logger.info('cron list before')
  for job in cron:
    print(job)

  # remove all pytrader cron jobs
  cron.remove_all(comment='pytrader')

  # sync exchanges at 6:05 am
  comment = f'pytrader'
  cmd = f'cd {cwd}; ./cronjob ./pytrade sync -r exchanges'
  job = cron.new(command=cmd, comment=comment)
  job.hour.every(1)
  job.hour.every(6)
  job.minute.on(5)

  # sync assets at 6:15 am
  comment = f'pytrader'
  cmd = f'cd {cwd}; ./cronjob ./pytrade sync -r assets'
  job = cron.new(command=cmd, comment=comment)
  job.hour.every(1)
  job.hour.every(6)
  job.minute.on(10)

  # sync etf holdings at 6:15 am
  comment = f'pytrader'
  cmd = f'cd {cwd}; ./cronjob ./pytrade sync -r etfholding'
  job = cron.new(command=cmd, comment=comment)
  job.hour.every(1)
  job.hour.every(6)
  job.minute.on(15)

  # sync digital asset price data for yesterday at 6:20 am
  comment = f'pytrader'
  cmd = f'cd {cwd}; ./cronjob ./pytrade download --asset digital --interval minute --start "28 hours ago" --end "1 hour ago"'
  job = cron.new(command=cmd, comment=comment)
  job.hour.every(1)
  job.hour.every(6)
  job.minute.on(20)

  # sync us_equity price data for yesterday at 6:30 am
  comment = f'pytrader'
  cmd = f'cd {cwd}; ./cronjob ./pytrade download --asset us_equity --interval minute --start "yesterday" --end "yesterday"'
  job = cron.new(command=cmd, comment=comment)
  job.hour.every(1)
  job.hour.every(6)
  job.minute.on(30)

  # sync redit mentions every hour
  comment = f'pytrader'
  cmd = f'cd {cwd}; ./cronjob ./pytrade sync -r wallstreetbets'
  job = cron.new(command=cmd, comment=comment)
  job.hour.every(1)
  job.minute.on(0)

  # # sync prices daily at 8:10 pm
  # comment = f'pytrader'
  # cmd = f'cd {cwd}; ./cronjob ./pytrade bars'
  # job = cron.new(command=cmd, comment=comment)
  # job.dow.on('MON', 'TUE', 'WED', 'THU', 'FRI')
  # job.hour.every(20)
  # job.minute.on(15)

  cron.write()

  logger.info('cron list after')
  for job in cron:
    print(job)
