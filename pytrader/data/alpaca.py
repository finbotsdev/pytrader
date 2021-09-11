# encoding: utf-8

from datetime import datetime, timedelta
import json
import pandas as pd
import pytrader.config as cfg
from pytrader.date import date
from pytrader.log import logger
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import time
import websocket

class AlpacaMarkets():

  def __init__(self):
    self.BASE_URL = cfg.get('APCA_API_BASE_URL')
    self.DATA_URL = cfg.get('APCA_API_DATA_URL')
    self.KEY_ID = cfg.get('APCA_API_KEY_ID')
    self.SECRET_KEY = cfg.get('APCA_API_SECRET_KEY')
    self.VERSION = cfg.get('APCA_API_VERSION')

    self.auth_header = {
      "APCA-API-KEY-ID": self.KEY_ID,
      "APCA-API-SECRET-KEY": self.SECRET_KEY
    }

  def _granularity(self, timeframe):
    if timeframe == '1Min':
      return 60
    if timeframe == '1Hour':
      return 60*60
    if timeframe == '1Day':
      return 60*60*24

  def get(self, path, **kwargs):
      params=[]
      for key, value in kwargs.items():
        params.append(f"{key}={value}")

      url = f"{self.BASE_URL}/{self.VERSION}/{path}"

      if params:
        url = "?".join([url, "&".join(params)])

      s = requests.Session()
      retries = Retry(total=5, backoff_factor=1, status_forcelist=[ 502, 503, 504 ])
      s.mount('https://', HTTPAdapter(max_retries=retries))
      r = s.get(url, headers=self.auth_header)

      if r.ok:
        return r.json()
      else:
        print(r.status_code, r.reason, url)

  def get_data(self, path, **kwargs):
      params=[]
      for key, value in kwargs.items():
        if kwargs[key]:
          params.append(f"{key}={value}")

      url = f"{self.DATA_URL}/{self.VERSION}/{path}"

      if params:
        url = "?".join([url, "&".join(params)])

      s = requests.Session()
      retries = Retry(total=5, backoff_factor=1, status_forcelist=[ 502, 503, 504 ])
      s.mount('https://', HTTPAdapter(max_retries=retries))
      r = s.get(url, headers=self.auth_header)

      if r.ok:
        return r.json()
      else:
        print(r.status_code, r.reason, url)

  # https://alpaca.markets/docs/api-documentation/api-v2/account/
  def get_account(self):
      return self.get(f"account")


  # https://alpaca.markets/docs/api-documentation/api-v2/account-configuration/
  # GET/v2/account/configurations
  # PATCH/v2/account/configurations


  # https://alpaca.markets/docs/api-documentation/api-v2/account-activities/
  # GET/v2/account/activities/{activity_type}
  # GET/v2/account/activities


  # https://alpaca.markets/docs/api-documentation/api-v2/assets/
  def get_assets(self):
      return self.get(f"assets")
  # GET/v2/assets/:id
  # GET/v2/assets/{symbol}


  # https://alpaca.markets/docs/api-documentation/api-v2/calendar/
  def get_calendar(self, start, end):
    """
    :param start: date - The first date to retrieve data for (inclusive)
    :param end: date - The last date to retrieve data for (inclusive)
    """
    return self.get('calendar', start=start, end=end)


  # https://alpaca.markets/docs/api-documentation/api-v2/clock/
  def get_clock(self):
    return self.get('clock')


  # https://alpaca.markets/docs/api-documentation/api-v2/orders/
  # GET/v2/orders
  # POST/v2/orders
  # GET/v2/orders/{order_id}
  # GET/v2/orders:by_client_order_id
  # PATCH/v2/orders/{order_id}
  # DELETE/v2/orders
  # DELETE/v2/orders/{order_id}


  # https://alpaca.markets/docs/api-documentation/api-v2/portfolio-history/
  # GET/v2/account/portfolio/history


  # https://alpaca.markets/docs/api-documentation/api-v2/positions/
  # GET/v2/positions
  # GET/v2/positions/{symbol}
  # DELETE/v2/positions
  # DELETE/v2/positions/{symbol}


  # https://alpaca.markets/docs/api-documentation/api-v2/market-data/alpaca-data-api-v2/historical/
  # GET/v2/stocks/{symbol}/trades
  # GET/v2/stocks/{symbol}/trades/latest
  # GET/v2/stocks/{symbol}/quotes
  # GET/v2/stocks/{symbol}/quotes/latest
  # GET/v2/stocks/{symbol}/bars
  def get_bars(self, symbol, start, end, timeframe='1Min', limit=None, page_token=None, adjustment='raw'):
    """
    :param symbol: string - The symbol to query for
    :param start: string (required) - Filter data equal to or after this time in RFC-3339 format. Fractions of a second are not accepted.
    :param end: string (required) - Filter data equal to or before this time in RFC-3339 format. Fractions of a second are not accepted.
    :param limit: int - Number of data points to return. Must be in range 1-10000, defaults to 1000.
    :param page_token: string - Pagination token to continue from.
    :param timeframe: string (required) - Timeframe for the aggregation. Values are customizeable, frequently used examples: 1Min, 15Min, 1Hour, 1Day.
    :param adjustment: string - Specifies the corporate action adjustment for the stocks. Enum: ‘raw’, ‘split’, ‘dividend’ or ‘all’. Default value is ‘raw’.
    """
    result = self.get_data(f"stocks/{symbol}/bars", start=start, end=end, timeframe=timeframe, limit=limit, page_token=page_token, adjustment=adjustment)

    if result and result['bars']:
      bars = result['bars']
    else:
      bars = []

    return bars

  def get_bars_chunked(self, symbol, start, end, timeframe='1Min', limit=10000, page_token=None, adjustment='raw'):
    # convert string dates to datetime objects
    start_time = datetime.strptime(start, '%Y-%m-%d')
    end_time = datetime.strptime(end, '%Y-%m-%d')
    print(f"start_time {type(start_time)} {start_time}")
    max_bars = limit
    max_time_seconds = max_bars * self._granularity(timeframe)
    delta = timedelta(seconds = max_time_seconds)
    chunk_end = start_time + delta

    # create a list of time chunks
    chunks = []
    while chunk_end < end_time:
      chunks.append(chunk_end)
      chunk_end = (chunk_end + delta)
    chunks.append(end_time)

    # fetch bar data in chunks
    bars = []
    for end_time in chunks:
      result = self.get_bars(symbol, end=end_time.date(), start=start_time.date(), timeframe=timeframe, limit=limit, page_token=page_token, adjustment=adjustment)
      logger.info(f'{symbol} - {start_time.date()} to {end_time.date()} - {len(result)} bars returned')
      bars.extend(result)
      start_time = end_time

    return bars

  # GET/v2/stocks/snapshots
  # GET/v2/stocks/{symbol}/snapshot


  # https://alpaca.markets/docs/api-documentation/api-v2/market-data/alpaca-data-api-v2/real-time/

  # https://alpaca.markets/docs/api-documentation/api-v2/watchlist/
  def get_watchlists(self):
    return self.get('watchlists')

  # GET/v2/watchlists/{watchlist_id}
  # PUT/v2/watchlists/{watchlist_id}
  # POST/v2/watchlists/{watchlist_id}
  # DELETE/v2/watchlists/{watchlist_id}
  # DELETE/v2/watchlists/{watchlist_id}/{symbol}
  # POST/v2/watchlists

  def exchange_map(self, symbol):
    """
    map alpaca exchange symbols to iex exchange symbols
    """
    exchanges = {
      'NASDAQ': 'XNGS',
      'ARCA': 'ARCX',
      'NYSE': 'ARCX',
      'AMEX': 'XASE',
      'BATS': 'BATS',
      'OTC': 'OTCM'
    }
    return exchanges[symbol]

class AlpacaDataframe():
  def __new__(cls, bars):
    df = pd.DataFrame(bars)
    df.set_axis(['dt', 'open', 'high', 'low', 'close', 'volume', 'n', 'vw'], axis=1, inplace=True)
    df["dt"] = pd.to_datetime((df["dt"]), format='%Y-%m-%dT%H:%M:%SZ')
    df.drop(labels=['n','vw'], axis=1, inplace=True)
    # add symbol column
    df.sort_values(by=['dt'], inplace=True)
    df.drop_duplicates(subset='dt', inplace=True)
    return df

class AlpacaStream():
  def __init__(self):
    self.DATA_URL = cfg.get('APCA_API_DATA_URL')
    self.KEY_ID = cfg.get('APCA_API_KEY_ID')
    self.SECRET_KEY = cfg.get('APCA_API_SECRET_KEY')
    self.VERSION = cfg.get('APCA_API_VERSION')

  def set_tickers(self, tickers: list):
    self.TICKERS = tickers

  def auth(self, ws):
    auth = {
      "action": "auth",
      "key": self.KEY_ID,
      "secret": self.SECRET_KEY
    }
    ws.send(json.dumps(auth))

  def subscribe(self, ws):
    message = {
      "action": "subscribe",
      "bars": ['*'],
      "dailyBars": ['*'],
      "lulds": ['*'],
      "quotes": self.TICKERS,
      "statuses": ['*'],
      "trades": self.TICKERS
    }
    ws.send(json.dumps(message))

  def on_open(self, ws):
    self.auth(ws)
    self.subscribe(ws)

  def on_message(self, ws, message):
    logger.info(message)

  def run(self):
    data_domain = self.DATA_URL.replace("https://","")
    endpoint = f"wss://stream.{data_domain}/v2/iex"
    ws = websocket.WebSocketApp(endpoint, on_open=self.on_open, on_message=self.on_message)
    ws.run_forever()

  def __repr__(self):
      return f'<AlpacaStream (tickers={self.TICKERS})>'
