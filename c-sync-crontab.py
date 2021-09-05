import config as cfg
from crontab import CronTab
import getpass
import os
import pytrader as pt
from pytrader.log import logger


"""
c-sync-crontab.py
---------------------
manage cron tasks
"""

def show_jobs():
  for job in cron:
      print(job)

def main(args):

  print('cron list before')
  show_jobs()

  # remove all pytrader cron jobs
  cron.remove_all(comment='pytrader')

  # say hellp
  comment = f'pytrader'
  cmd = f'cd {cwd}; ./cronjob c-hello.py'
  job = cron.new(command=cmd, comment=comment)
  job.day.every(1)
  job.hour.every(1)
  job.minute.on(0)

  # sync assets at 8:00 pm
  comment = f'pytrader'
  cmd = f'cd {cwd}; ./cronjob c-sync-assets.py'
  job = cron.new(command=cmd, comment=comment)
  job.dow.on('MON', 'TUE', 'WED', 'THU', 'FRI')
  job.hour.every(20)
  job.minute.on(0)

  # sync etf holdings at 8:05 pm
  comment = f'pytrader'
  cmd = f'cd {cwd}; ./cronjob c-sync-etfholdings.py'
  job = cron.new(command=cmd, comment=comment)
  job.dow.on('MON', 'TUE', 'WED', 'THU', 'FRI')
  job.hour.every(20)
  job.minute.on(5)

  # sync prices daily at 8:10 pm
  comment = f'pytrader'
  cmd = f'cd {cwd}; ./cronjob c-sync-prices.py'
  job = cron.new(command=cmd, comment=comment)
  job.dow.on('MON', 'TUE', 'WED', 'THU', 'FRI')
  job.hour.every(20)
  job.minute.on(10)

  # sync redit mentions every hour
  comment = f'pytrader'
  cmd = f'cd {cwd}; ./cronjob c-sync-redit-mentions.py'
  job = cron.new(command=cmd, comment=comment)
  job.hour.every(1)
  job.minute.on(0)

  cron.write()

  print('cron list after')
  show_jobs()

if __name__ == '__main__':
  timer = pt.Timer()

  parser = pt.ArgumentParser()
  parser.add_argument("-v", "--verbose", action='store_true', help="verbose")

  args = parser.parse_args()

  logger.info(f'pytrader {__file__}')

  current_user = getpass.getuser()
  cwd = os.getcwd()
  cron = CronTab(user=current_user)

  main(args)

  timer.report()
