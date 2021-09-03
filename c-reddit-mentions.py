import config as cfg
from datetime import datetime, date, time
from psaw import PushshiftAPI
import psycopg2 as pg
import psycopg2.extras as pgx

connection = pg.connect(dsn=cfg.DSN, cursor_factory=pgx.DictCursor)
cursor = connection.cursor()

api = PushshiftAPI()

start_time = int(datetime.combine(date.today(), time()).timestamp())

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
                    SELECT * FROM stocks WHERE symbol = %s
                """, (cashtag[1:],))
                stock = cursor.fetchone()
                if stock:
                    cursor.execute("""
                        INSERT INTO mentions (stock_id, dt, message, source, url)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (stock['id'], datetime.fromtimestamp(submission.created_utc), submission.title, 'reddit', submission.url))
                    connection.commit()

            except Exception as e:
              connection.rollback();

cashtags = list(set(filter(lambda word: word.lower().startswith('$'), words)))
print(f"\n Cashtags Mentioned")
print(cashtags)

