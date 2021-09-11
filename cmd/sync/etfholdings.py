# encoding: utf-8

import datetime as dt
import os
import pytrader as pt
from pytrader.csv import is_comment, is_whitespace, read_and_filter_csv
from pytrader.data import AlpacaMarkets, CoinbasePro
from pytrader.database import Session
from pytrader.log import logger
from pytrader.model import Asset, EtfHolding
import requests
import traceback


"""
etf_holding.py
---------------------
sync etf holding records
"""


def main(args):
  print(args)

  try:
    logger.info('maintain crypto resources')

    session = Session()

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

    today = dt.date.today().strftime('%Y-%m-%d')
    etf_symbols = [key for key in feeds]

    for asset in session.query(Asset).filter(Asset.symbol.in_(etf_symbols)):
      asset.is_etf = True

    session.commit()

    for etf in session.query(Asset).filter(Asset.is_etf == True):
      logger.info(f"Download Holdings Report for {etf.name} ({etf.symbol})")

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
          session.rollback()
          logger.error(e)
          print(e)

      else:
          logger.info(f"{etf.symbol} does not exist in feeds dict")

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
