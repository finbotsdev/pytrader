# encoding: utf-8

import base64
import hashlib
import hmac
import json
import pytrader.config as cfg
import requests
from requests.auth import AuthBase
import time
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

    r = requests.get(url, auth=auth)

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
    """
    return self.get(f"products/{product_id}/candles", start=start, end=end, granularity=granularity)
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

class CoinbaseProStream():
  def __init__(self):
    self.URL = cfg.get('COINBASEPRO_API_STREAM')
    self.KEY_ID = cfg.get('COINBASEPRO_API_KEY_ID')
    self.SECRET_KEY = cfg.get('COINBASEPRO_API_SECRET_KEY')
    self.PASSWORD = cfg.get('COINBASEPRO_API_PASSWORD')

  def subscribe(self, ws):
    sub_params = {
      "type": "subscribe",
      "product_ids": [
        "ETH-USD"
      ],
      "channels": [
        {
          "name": "ticker",
          "product_ids": [
            "ETH-USD"
          ]
        }
      ]
    }
    timestamp = str(time.time())
    message = timestamp + 'GET' + '/users/self/verify'
    auth_headers = get_auth_headers(message, timestamp)
    sub_params['signature'] = auth_headers['CB-ACCESS-SIGN']
    sub_params['key'] = auth_headers['CB-ACCESS-KEY']
    sub_params['passphrase'] = auth_headers['CB-ACCESS-PASSPHRASE']
    sub_params['timestamp'] = auth_headers['CB-ACCESS-TIMESTAMP']
    ws.send(json.dumps(sub_params))

  def on_open(self, ws):
    self.subscribe(ws)

  def on_message(self, ws, message):
    print(message)

  def run(self):
    ws = websocket.WebSocketApp(self.URL, on_open=self.on_open, on_message=self.on_message)
    ws.run_forever()

  def __repr__(self):
      return f'<CoinbaseProStream >'

def get_auth_headers(message, timestamp):
    message = message.encode('ascii')
    hmac_key = base64.b64decode(cfg.get('COINBASEPRO_API_SECRET_KEY'))
    signature = hmac.new(hmac_key, message, hashlib.sha256)
    signature_b64 = base64.b64encode(signature.digest()).decode('utf-8')
    return {
        'Content-Type': 'Application/JSON',
        'CB-ACCESS-SIGN': signature_b64,
        'CB-ACCESS-TIMESTAMP': timestamp,
        'CB-ACCESS-KEY': cfg.get('COINBASEPRO_API_KEY_ID'),
        'CB-ACCESS-PASSPHRASE': cfg.get('COINBASEPRO_API_PASSWORD')
    }
