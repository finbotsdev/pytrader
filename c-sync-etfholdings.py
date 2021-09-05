import config as cfg
import csv
from datetime import date
import os
import psycopg2 as pg
import psycopg2.extras as pgx
import pytrader as pt
import pytrader.log as log
import requests
import sqlalchemy as sa
from sqlalchemy import exc

from model import Session
from model.asset import Asset
from model.etf_holding import EtfHolding
"""
c-sync-etfholdings.py
---------------------
grab lists of holdings from various etfs
maintain a local db of etf holdings so that we can observe changes over time

"""

timer = pt.Timer()

logger = log.logging
log.config_root_logger()

session = Session()

# store a dictionary of feed urls keyed by ticker symbol
feeds = {
    "ARKK": "https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_INNOVATION_ETF_ARKK_HOLDINGS.csv",
    "ARKQ": "https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_AUTONOMOUS_TECHNOLOGY_&_ROBOTICS_ETF_ARKQ_HOLDINGS.csv",
    "ARKW": "https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_NEXT_GENERATION_INTERNET_ETF_ARKW_HOLDINGS.csv",
    "ARKG": "https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_GENOMIC_REVOLUTION_MULTISECTOR_ETF_ARKG_HOLDINGS.csv",
    "ARKF": "https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_FINTECH_INNOVATION_ETF_ARKF_HOLDINGS.csv",
    "ARKX": "https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_SPACE_EXPLORATION_&_INNOVATION_ETF_ARKX_HOLDINGS.csv",
    "IZRL": "https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_ISRAEL_INNOVATIVE_TECHNOLOGY_ETF_IZRL_HOLDINGS.csv",
    "PRNT": "https://ark-funds.com/wp-content/fundsiteliterature/csv/THE_3D_PRINTING_ETF_PRNT_HOLDINGS.csv",
}

# Real comments are more complicated ...
def is_comment(line):
    return line.startswith('#')

# Kind of sily wrapper
def is_whitespace(line):
    return line.isspace()

def iter_filtered(in_file, *filters):
    for line in in_file:
        if not any(fltr(line) for fltr in filters):
            yield line

# A dis-advantage of this approach is that it requires storing rows in RAM
# However, the largest CSV files I worked with were all under 100 Mb
def read_and_filter_csv(csv_path, *filters):
    with open(csv_path, 'r') as fin:
        iter_clean_lines = iter_filtered(fin, *filters)
        reader = csv.DictReader(iter_clean_lines, delimiter=',')
        return [row for row in reader]


def main(args):
  print(args)

  today = date.today().strftime('%Y-%m-%d')

  try:
    known_etfs = ['ARKF', 'ARKG', 'ARKK', 'ARKQ', 'ARKX', 'IRZL', 'PRNT']
    for asset in session.query(Asset).filter(Asset.symbol.in_(known_etfs)):
      asset.is_etf = True
    session.commit()

    for etf in session.query(Asset).filter(Asset.is_etf == True):
      logger.info(f"Download Holdings Report for {etf.company} ({etf.symbol})")

      # create directory to store download files
      dirname = os.path.dirname(__file__)
      filepath = os.path.join(dirname, '.data', 'holdings', today)
      os.path.dirname(__file__)
      os.makedirs(filepath, exist_ok=True)

      # download updated csv file for fund
      if etf.symbol in feeds.keys():
        url = feeds[etf.symbol]
        logger.info(f"    {url}")

        hfile = f"{filepath}/ETF_{etf.symbol}_HOLDINGS.csv"

        headers = {
          'User-Agent': 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        }

        with requests.get(url, headers=headers, stream=True) as r:
          r.raise_for_status()
          with open(hfile, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
              f.write(chunk)

        try:
          for l in read_and_filter_csv(hfile, is_comment, is_whitespace):
            if l['date'] and l['ticker'] and l['shares'] and l['weight(%)']:
              holding = session.query(Asset).filter(Asset.symbol == l['ticker']).first()
              if holding:
                logger.info(f"    {etf.symbol} holds {l['shares']} shares of {holding.symbol} which is {l['weight(%)']}% of their holdings")
                eft_holding = EtfHolding(
                  etf_id=etf.id,
                  holding_id=holding.id,
                  dt=l['date'],
                  shares=l['shares'],
                  weight=l['weight(%)'],
                )
                session.add(eft_holding)
          session.commit()
        except Exception as e:
          logger.error(e)
          print(e)

      else:
          logger.info(f"{etf.symbol} does not exist in feeds dict")

  except Exception as e:
    logger.error(e)
    print(e)
    pass


if __name__ == '__main__':
  parser = pt.ArgumentParser()
  parser.add_argument("-v", "--verbose", action='store_true', help="verbose")

  args = parser.parse_args()

  logger.info('pytrader initializing')

  main(args)

  timer.report()
