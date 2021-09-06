# encoding: utf-8

import config as cfg
import pytrader as pt
from pytrader.log import logger
from pytrader.event import notify_email
import traceback


"""
c-notify.py
---------------------
dispatch event notification
"""


def main(args):
  print(args)

  try:
    logger.info('send event notifications')

    message = [
      'Bacon ipsum dolor amet shank cow ham hock drumstick, pancetta doner pork loin chicken tenderloin salami short ribs pork pastrami tri-tip. Doner prosciutto bresaola, leberkas pork tongue pork chop. Shoulder shank pork loin drumstick. Fatback brisket hamburger pork, jowl tenderloin bacon swine tri-tip cupim. Pork chop chuck salami, pork loin porchetta bacon corned beef ball tip shankle. Tail kielbasa capicola landjaeger, strip steak pastrami venison boudin picanha fatback rump tenderloin sirloin bacon biltong.',
      'Short loin biltong cupim burgdoggen boudin swine leberkas doner. Tongue meatball strip steak, sirloin ham kielbasa pork loin ham hock. Meatloaf ribeye turducken cupim, picanha ham fatback spare ribs tri-tip sausage shankle alcatra kevin kielbasa. Landjaeger meatball tongue porchetta pastrami. Landjaeger meatball ground round, rump tri-tip picanha tongue doner jowl beef ribs ham hock bresaola shank flank. Cow t-bone pork loin shankle jowl flank venison.',
    ]

    notify_email('eventname', message)

  except Exception as e:
    logger.error(e)
    print(e)
    print(traceback.format_exc())
    pass


if __name__ == '__main__':
  parser = pt.ArgumentParser()
  parser.add_argument("-v", "--verbose", action='store_true', help="verbose")
  args = parser.parse_args()

  timer = pt.Timer()
  logger.info(f'pytrader {__file__}')
  main(args)
  timer.report()
