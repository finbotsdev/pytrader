# encoding: utf-8

import base64
from datetime import datetime, timedelta, timezone
import hashlib
import hmac
import json
import pandas as pd
import pytrader.config as cfg
from pytrader.log import logger
import requests
from requests.adapters import HTTPAdapter
from requests.auth import AuthBase
from requests.packages.urllib3.util.retry import Retry
import time
import traceback
import websocket

class CoinbaseExchangeAuth(AuthBase):

    def __init__(self):
        self.api_key = cfg.get('COINBASEPRO_API_KEY_ID')
        self.secret_key = cfg.get('COINBASEPRO_API_SECRET_KEY')
        self.passphrase = cfg.get('COINBASEPRO_API_PASSWORD')

    def __call__(self, request):
        timestamp = str(time.time())
        message = timestamp + request.method + request.path_url + (request.body or '')
        hmac_key = base64.b64decode(self.secret_key)
        signature = hmac.new(hmac_key, message.encode('utf-8'), hashlib.sha256)
        signature_b64 = base64.b64encode(signature.digest())

        request.headers.update({
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        })
        return request

class CoinbasePro():

  def __init__(self):
    self.URL = cfg.get('COINBASEPRO_API_URL')

  def get(self, path, **kwargs):
    params=[]
    for key, value in kwargs.items():
      if value:
        params.append(f"{key}={value}")

    url = f"{self.URL}/{path}"

    if params:
      url = "?".join([url, "&".join(params)])

    auth = CoinbaseExchangeAuth()

    s = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[ 502, 503, 504 ])
    s.mount('https://', HTTPAdapter(max_retries=retries))
    r = s.get(url, auth=auth)

    if r.ok:
      return r.json()
    else:
      print(r.status_code, r.reason, url)

  # GET /accounts
  def get_accounts(self):
    return self.get(f"accounts")
  # GET /accounts/<account-id>
  # GET /accounts/<account-id>/ledger
  # GET /accounts/<account_id>/holds

  # GET /coinbase-accounts
  # POST /coinbase-accounts/<coinbase-account-id>/addresses

  # POST /conversions

  # GET /currencies
  def get_currencies(self):
    return self.get(f"currencies")
  # GET /currencies/<id>

  # POST /deposits/coinbase-account
  # POST /deposits/payment-method

  # GET /fees
  def get_fees(self):
    return self.get(f"fees")

  # GET /fills
  def get_fills(self):
    return self.get(f"fills")

  # GET /orders
  def get_orders(self):
    return self.get(f"orders")
  # GET /orders/<id>
  # GET /orders/client:<client_oid>
  # POST /orders
  # DELETE /orders
  # DELETE /orders/<id>
  # DELETE /orders/client:<client_oid>

  # GET /payment-methods
  def get_payment_methods(self):
    return self.get(f"payment-methods")

  # GET /products
  def get_products(self):
    return self.get(f"products")
  # GET /products/<product-id>
  def get_product(self, product_id):
    return self.get(f"products/{product_id}")
  # GET /products/<product-id>/book
  def get_product_book(self, product_id):
    return self.get(f"products/{product_id}/book")
  # GET /products/<product-id>/ticker
  def get_product_ticker(self, product_id):
    return self.get(f"products/{product_id}/ticker")
  # GET /products/<product-id>/trades
  def get_product_trades(self, product_id):
    return self.get(f"products/{product_id}/trades")
  # GET /products/<product-id>/candles
  def get_product_candles(self, product_id, start=None, end=None, granularity=60):
    """
    :param start:	str - Start time in ISO 8601 (2021-09-07)
    :param end:	str - End time in ISO 8601 (2021-09-07)
    :param granularity:	int - Desired timeslice in seconds

    If either one of the start or end fields are not provided then both fields will be ignored.
    If a custom time range is not declared then one ending now is selected.

    The maximum number of data points for a single request is 300 candles.
    If your selection of start/end time and granularity will result in more than 300 data points,
    your request will be rejected.

    If you wish to retrieve fine granularity data over a larger time range,
    you will need to make multiple requests with new start/end ranges.

    at 60 second granularity this means a maximum of 5 hours worth of data
    couple that with the start and end parameters being dates and not datetimes
    there is no way to retrieve complete historical data at minute granularity
    """
    return self.get(f"products/{product_id}/candles", start=start, end=end, granularity=granularity)

  def get_product_candles_chunked(self, product_id, start=None, end=None, granularity=60):
    start_time = datetime.strptime(start, '%Y-%m-%d')
    end_time = datetime.strptime(end, '%Y-%m-%d')

    # response can include max 300 bars
    # calculate the max timeframe we can request
    # so that request shuuld return no more than 300 bars
    max_bars = 275
    max_time_seconds = max_bars * granularity
    delta = timedelta(seconds = max_time_seconds)
    chunk_end = start_time + delta

    # create a list of time chunks
    chunks = []
    while chunk_end < end_time:
      chunks.append(chunk_end)
      chunk_end = chunk_end + delta
    chunks.append(end_time)

    bars = []
    for end_time in chunks:
      result = self.get_product_candles(product_id, start=start_time, end=end_time, granularity=granularity)
      if result:
        logger.info(f'{product_id} - {start_time} to {end_time} - {len(result)} bars returned')
        bars.extend(result)
      start_time = end_time

    return bars

  # GET /products/<product-id>/stats
  def get_product_stats(self, product_id):
    return self.get(f"products/{product_id}/stats")

  # GET /profiles
  def get_profiles(self):
    return self.get(f"profiles")
  # GET /profiles/<profile_id>
  # POST /profiles/transfer

  # GET /reports
  def get_reports(self):
    return self.get(f"reports")
  # POST /reports
  # GET /reports/:report_id

  # GET /time
  def get_time(self):
    return self.get(f"time")

  # GET /transfers
  def get_transfers(self):
    return self.get(f"transfers")
  # GET /transfers/:transfer_id

  # GET /users/self/exchange-limits
  def get_exchange_limits(self):
    return self.get(f"users/self/exchange-limits")

  # GET /users/self/verify
  def get_user_verify(self):
    return self.get(f"users/self/verify")

  # POST /withdrawals/coinbase-account
  # POST /withdrawals/crypto
  # GET /withdrawals/fee-estimate
  # POST /withdrawals/payment-method

class CoinbaseProDataFrame():
  def __new__(cls, bars):
    df = pd.DataFrame(bars)
    df.set_axis(['dt', 'open', 'high', 'low', 'close', 'volume'], axis=1, inplace=True)
    df["dt"] = pd.to_datetime(df["dt"], unit='s')
    df.sort_values(by=['dt'], inplace=True)
    df.drop_duplicates(subset='dt', inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df

class CoinbaseProStream():
  def __init__(self):
    self.URL = cfg.get('COINBASEPRO_API_STREAM')
    self.KEY_ID = cfg.get('COINBASEPRO_API_KEY_ID')
    self.SECRET_KEY = cfg.get('COINBASEPRO_API_SECRET_KEY')
    self.PASSWORD = cfg.get('COINBASEPRO_API_PASSWORD')
    self.message_count = 0
    self.messages_minute = 0

    self.bars = {}

  def auth_headers(self, message, timestamp):
    message = message.encode('ascii')
    hmac_key = base64.b64decode(self.SECRET_KEY)
    signature = hmac.new(hmac_key, message, hashlib.sha256)
    signature_b64 = base64.b64encode(signature.digest()).decode('utf-8')
    return {
      'Content-Type': 'Application/JSON',
      'CB-ACCESS-SIGN': signature_b64,
      'CB-ACCESS-TIMESTAMP': timestamp,
      'CB-ACCESS-KEY': self.KEY_ID,
      'CB-ACCESS-PASSPHRASE': self.PASSWORD
    }

  def subscribe(self, ws):
    params = {
      "type": "subscribe",
      "product_ids": [
        "BTC-USD",
        "ETH-USD",
        "LTC-USD"
      ],
      "channels": [
        {
          "name": "matches",
          "product_ids": [
            "BTC-USD",
            "ETH-USD",
            "LTC-USD"
          ]
        }
      ]
    }
    timestamp = str(time.time())
    message = timestamp + 'GET' + '/users/self/verify'
    auth = self.auth_headers(message, timestamp)
    params['signature'] = auth['CB-ACCESS-SIGN']
    params['key'] = auth['CB-ACCESS-KEY']
    params['passphrase'] = auth['CB-ACCESS-PASSPHRASE']
    params['timestamp'] = auth['CB-ACCESS-TIMESTAMP']
    ws.send(json.dumps(params))

  def on_open(self, ws):
    self.subscribe(ws)

  def on_message(self, ws, message):
    self.message_count += 1
    self.messages_minute += 1
    try:
      msg = json.loads(message)

      if msg["type"] == "match":

        trade_id = msg["trade_id"]
        price = msg["price"]
        product = msg["product_id"]
        sequence = msg["sequence"]
        size = msg["size"]
        time = msg["time"] # str formatted 2021-09-08T02:06:43.833769Z
        t = datetime.strptime(time, '%Y-%m-%dT%H:%M:%S.%fZ') # convert to datetime object
        t = self.utc_to_local(t)
        dt = t.strftime("%Y-%m-%d %H:%M:00") # convert to minute timestamp

        if not product in self.bars.keys():
          self.bars[product] = {}

        prodbars = self.bars[product]

        if dt in prodbars.keys():
          # update current dt dict for product/minute
          prodbars[dt] = {
            "open": prodbars[dt]['open'],
            "high": max(float(price), prodbars[dt]['high']),
            "low": min(float(price), prodbars[dt]['low']),
            "close": float(price),
            "volume": float(size) + prodbars[dt]['volume']
          }
        else:
          # start new dt dict for product/minute
          self.message_minute = 0
          prodbars[dt] = {
            "open": float(price),
            "high": float(price),
            "low": float(price),
            "close": float(price),
            "volume": float(size)
          }

        print(f'{self.messages_minute} ------------------------------------ {self.message_count}')
        for product in self.bars:
          for dt in self.bars[product]:
            print(f'{dt} {product} {self.bars[product][dt]}')

      """
      subscribe to the 'matches' channel, and create a candle on your own from the data.
      Create four variables (Open, High, Low, Close),
      store the first price that occurs in a slice of time (in your case, an hour),
      then store the max and min prices seen during the slice of time,
      and finally the last price seen.
      You can also keep a running summation of the volume during the time window.
      """

      # https://www.youtube.com/watch?v=ER7Va1qdURw

      # {
      #   "type":"match",
      #   "trade_id":153238342,
      #   "maker_order_id":"8c85395d-7a15-43eb-855a-d721520fe69e",
      #   "taker_order_id":"87436bd7-ec44-4b34-abe2-bce0a7c66d55",
      #   "side":"sell",
      #   "size":"0.00038418",
      #   "price":"3480.06",
      #   "product_id":"ETH-USD",
      #   "sequence":20563024039,
      #   "time":"2021-09-08T01:42:32.206104Z"
      # }

    except Exception as e:
      print(e)
      print(e)
      print(message)
      print(traceback.format_exc())

  def utc_to_local(self, utc_dt):
      return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

  def run(self):
    ws = websocket.WebSocketApp(self.URL, on_open=self.on_open, on_message=self.on_message)
    ws.run_forever()

  def __repr__(self):
      return f'<CoinbaseProStream >'
