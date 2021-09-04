import config as cfg
from datetime import datetime, date, time
from psaw import PushshiftAPI
import psycopg2 as pg
import psycopg2.extras as pgx
import pytrader as pt
from pytrader.data import AlpacaMarkets, date
import pytrader.log as log

timer = pt.Timer()

logger = log.logging
log.config_root_logger()

connection = pg.connect(dsn=cfg.DSN, cursor_factory=pgx.DictCursor)
cursor = connection.cursor()

api = PushshiftAPI()

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
        print(f"\n{submission.created_utc} - {submission.title} ({submission.author})")
        print(submission.url)

        for cashtag in cashtags: # iterate cashtags in submisstion title
            try:
                cursor.execute("""
                    SELECT * FROM asset WHERE symbol = %s
                """, (cashtag[1:],))
                asset = cursor.fetchone()
                if asset:
                    cursor.execute("""
                        INSERT INTO mention (asset_id, dt, message, source, url)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (asset['id'], datetime.fromtimestamp(submission.created_utc), submission.title, 'reddit', submission.url))
                    connection.commit()

            except Exception as e:
              connection.rollback();

logger.info('get cashtags from submissions')

cashtags = list(set(filter(lambda word: word.lower().startswith('$'), words)))
print(f"Cashtags Mentioned {cashtags}")

timer.report()
