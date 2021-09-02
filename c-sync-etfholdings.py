import config as cfg
import csv
from datetime import date
import os
import psycopg2 as pg
import psycopg2.extras as pgx
import requests
# import urllib.request

"""
c-sync-etfholdings.py
---------------------
grab lists of holdings from various etfs
maintain a local db of etf holdings so that we can observe changes over time

"""


connection = pg.connect(dsn=cfg.DSN, cursor_factory=pgx.DictCursor)
cursor = connection.cursor()
today = date.today()

# store a dictionary of feed urls keyed by ticker symbol
feeds = {
    "ARKK": "https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_INNOVATION_ETF_ARKK_HOLDINGS.csv",
    "ARKQ": "https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_AUTONOMOUS_TECHNOLOGY_&_ROBOTICS_ETF_ARKQ_HOLDINGS.csv",
    "ARKW": "https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_NEXT_GENERATION_INTERNET_ETF_ARKW_HOLDINGS.csv",
    "ARKG": "https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_GENOMIC_REVOLUTION_MULTISECTOR_ETF_ARKG_HOLDINGS.csv",
    "ARKF": "https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_FINTECH_INNOVATION_ETF_ARKF_HOLDINGS.csv",
    "ARKX": "https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_SPACE_EXPLORATION_&_INNOVATION_ETF_ARKX_HOLDINGS.csv",
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

cursor.execute("""
    UPDATE stocks SET is_etf = TRUE WHERE symbol IN ('ARKF', 'ARKG', 'ARKK', 'ARKQ', 'ARKX', 'IRZL', 'PRNT')
""")
connection.commit()

cursor.execute("SELECT * FROM stocks WHERE is_etf = TRUE")
etfs = cursor.fetchall()

for etf in etfs:
    print(f"Download Holdings Report for {etf['company']} ({etf['symbol']})")

    # create directory to store download files
    dirname = os.path.dirname(__file__)
    filepath = os.path.join(dirname, '.data', 'holdings', today.strftime('%Y-%m-%d'))
    os.path.dirname(__file__)
    os.makedirs(filepath, exist_ok=True) 

    # download updated csv file for fund
    if etf['symbol'] in feeds.keys():
        url = feeds[etf['symbol']]
        print(f"    {url}")

        hfile = f"{filepath}/ETF_{etf['symbol']}_HOLDINGS.csv"

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
                    cursor.execute("""
                        SELECT * FROM stocks WHERE symbol = %s
                    """, (l['ticker'],))
                    holding = cursor.fetchone()
                    if holding:
                        print(f"    {etf['symbol']} holds {l['shares']} shares of {holding['symbol']} which is {l['weight(%)']}% of their holdings")
                        cursor.execute("""
                            INSERT INTO etfs_holdings ( etf_id, holding_id, dt, shares, weight )
                            VALUES (%s, %s, %s, %s, %s)
                        """, (etf[0], holding[0], l['date'], l['shares'], l['weight(%)']))
            connection.commit()
        except Exception as e:
            print(e)

    else:
        print(f"{etf['symbol']} does not exist in feeds dict")
