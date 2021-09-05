import config as cfg
from datetime import datetime, date, time
from psaw import PushshiftAPI
import pytrader as pt
from pytrader.log import logger
import sqlalchemy as sa
from sqlalchemy import exc

from model import Session
from model.asset import Asset
from model.mention import Mention


"""
c-sync-reddit-mentions.py
---------------------
inspect posts from subredit wallstreetbets
record observed cashtags
"""


api = PushshiftAPI()
session = Session()


def main(args):
  print(args)

  start_time = int(datetime.combine(date.today(), time()).timestamp())

  logger.info('search_submissions')
  submissions = api.search_submissions(after=start_time,
                                      subreddit='wallstreetbets',
                                      filter=['url','author', 'title', 'subreddit'],
                                      limit=50)

  words = [] # list to hold submission title words
  for submission in submissions:
    sub_words = submission.title.split()
    words.extend(sub_words)
    cashtags = list(set(filter(lambda word: word.lower().startswith('$'), sub_words)))
    if cashtags:
      logger.info(f"\n{submission.created_utc} - {submission.title} ({submission.author})")
      logger.info(submission.url)

      for cashtag in cashtags: # iterate cashtags in submisstion title
        try:
          symbol = cashtag[1:]
          asset = session.query(Asset).filter(Asset.symbol == symbol).first()

          if asset:
            mention = Mention(
              asset_id=asset.id,
              dt=datetime.fromtimestamp(submission.created_utc),
              message=submission.title,
              source='reddit',
              url=submission.url
            )
            session.add(mention)
            session.commit()

        except Exception as e:
          logger.error(e)
          print(e)
          session.rollback()

  logger.info('get cashtags from submissions')
  cashtags = list(set(filter(lambda word: word.lower().startswith('$'), words)))

  logger.info(f"Cashtags Mentioned {cashtags}")


if __name__ == '__main__':
  parser = pt.ArgumentParser()
  parser.add_argument("-v", "--verbose", action='store_true', help="verbose")
  args = parser.parse_args()

  timer = pt.Timer()
  logger.info(f'pytrader {__file__}')
  main(args)
  timer.report()
