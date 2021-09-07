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

  def _get(self, path):
    url = f"{self.URL}/{path}"
    r = requests.get(url)

    if r.ok:
      return r.json()
    else:
      print(r.status_code, r.reason, url)

  def get(self, path, **kwargs):
    params=[]
    for key, value in kwargs.items():
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
  # GET /currencies/<id>
  # POST /deposits/coinbase-account
  # POST /deposits/payment-method
  # GET /fees
  # GET /fills
  # GET /orders
  # GET /orders/<id>
  # GET /orders/client:<client_oid>
  # POST /orders
  # DELETE /orders
  # DELETE /orders/<id>
  # DELETE /orders/client:<client_oid>
  # GET /payment-methods
  # GET /products
  # GET /products/<product-id>
  # GET /products/<product-id>/book
  # GET /products/<product-id>/ticker
  # GET /products/<product-id>/trades
  # GET /products/<product-id>/candles
  # GET /products/<product-id>/stats
  # GET /profiles
  # GET /profiles/<profile_id>
  # POST /profiles/transfer
  # GET /reports
  def get_reports(self):
      return self.get(f"reports")

  # POST /reports
  # GET /reports/:report_id
  # GET /time
  def get_time(self):
      return self._get(f"time")

  # GET /transfers
  # GET /transfers/:transfer_id
  # GET /users/self/exchange-limits
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

  def auth(self, ws):
    pass

  def subscribe(self, ws):
    pass

  def on_open(self, ws):
    self.auth(ws)
    self.subscribe(ws)

  def on_message(self, ws, message):
    print(message)

  def run(self):
    ws = websocket.WebSocketApp(self.URL, on_open=self.on_open, on_message=self.on_message)
    ws.run_forever()

  def __repr__(self):
      return f'<CoinbaseProStream >'
