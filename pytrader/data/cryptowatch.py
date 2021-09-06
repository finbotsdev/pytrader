# encoding: utf-8

import json
import pytrader.config as cfg
import requests
import websocket

class Cryptowatch():

  def __init__(self):
    self.URL = cfg.get('CRYPTOWATCH_API_URL')
    self.KEY_ID = cfg.get('CRYPTOWATCH_API_KEY_ID')
    self.SECRET_KEY = cfg.get('CRYPTOWATCH_API_SECRET_KEY')

    self.auth_header = {
      "X-CW-API-Key": self.KEY_ID
    }

  def get(self, path, **kwargs):
      params=[]
      for key, value in kwargs.items():
        params.append(f"{key}={value}")

      url = f"{self.URL}/{path}"

      if params:
        url = "?".join([url, "&".join(params)])

      r = requests.get(url, headers=self.auth_header)

      if r.ok:
        return r.json()
      else:
        print(r.status_code, r.reason, url)

  # https://docs.cryptowat.ch/rest-api/assets/assets-index
  # GET /assets
  def get_assets(self):
    return self.get(f"assets")

  # https://docs.cryptowat.ch/rest-api/assets/details
  # GET /assets/:asset
  def get_asset(self, asset):
    return self.get(f"assets/{asset}")

  # https://docs.cryptowat.ch/rest-api/exchanges/exchanges-index
  # GET /exchanges
  def get_exchanges(self):
    return self.get(f"exchanges")

  # https://docs.cryptowat.ch/rest-api/exchanges/details
  # GET /exchanges/:exchange
  def get_exchange(self, exchange):
    return self.get(f"exchanges/{exchange}")

  # https://docs.cryptowat.ch/rest-api/exchanges/markets
  # GET /markets/:exchange
  def get_exchange_markets(self, exchange):
    return self.get(f"exchanges/{exchange}/markets")

  # https://docs.cryptowat.ch/rest-api/pairs/pairs-index
  # GET /pairs
  def get_pairs(self):
    return self.get(f"pairs")

  # https://docs.cryptowat.ch/rest-api/pairs/details
  # GET /pairs/:asset
  def get_pair(self, asset):
    return self.get(f"pairs/{asset}")

  # https://docs.cryptowat.ch/rest-api/markets/markets-index
  # GET /markets
  def get_markets(self):
    return self.get(f"markets")

  # https://docs.cryptowat.ch/rest-api/markets/details
  # GET /markets/:exchange/:pair
  def get_market(self, exchange, pair,):
    return self.get(f"markets/{exchange}/{pair}")

  # https://docs.cryptowat.ch/rest-api/markets/price
  # GET /markets/:exchange/:pair/price
  def get_market_price(self, exchange, pair,):
    return self.get(f"markets/{exchange}/{pair}/price")

  # https://docs.cryptowat.ch/rest-api/markets/trades
  # GET /markets/:exchange/:pair/trades
  def get_market_trades(self, exchange, pair,):
    return self.get(f"markets/{exchange}/{pair}/trades")

  # https://docs.cryptowat.ch/rest-api/markets/summary
  # GET /markets/:exchange/:pair/summary
  def get_market_summary(self, exchange, pair,):
    return self.get(f"markets/{exchange}/{pair}/summary")

  # https://docs.cryptowat.ch/rest-api/markets/orderbook
  # GET /markets/:exchange/:pair/orderbook
  def get_market_orderbook(self, exchange, pair,):
    return self.get(f"markets/{exchange}/{pair}/orderbook")

  # https://docs.cryptowat.ch/rest-api/markets/ohlc
  # GET /markets/:exchange/:pair/ohlc
  def get_market_ohlc(self, exchange, pair,):
    return self.get(f"markets/{exchange}/{pair}/ohlc")


class CryptowatchStream():

  def __init__(self):
    self.URL = cfg.get('CRYPTOWATCH_API_STREAM_URL')
    self.KEY_ID = cfg.get('CRYPTOWATCH_API_KEY_ID')
    self.SECRET_KEY = cfg.get('CRYPTOWATCH_API_SECRET_KEY')
    self.VERSION = cfg.get('CRYPTOWATCH_API_VERSION')

  def subscribe(self, ws):
    message = {
      "subscribe": {
        "subscriptions": [
          { "streamSubscription": { "resource": "pairs:9:ohlc" } },
          { "streamSubscription": { "resource": "pairs:125:ohlc" } }
        ]
      }
    }
    ws.send(json.dumps(message))

  def on_open(self, ws):
    self.subscribe(ws)

  def on_message(self, ws, message):
    print(message)

    # {
    #   "marketUpdate":{
    #     "market":{
    #       "exchangeId":"10",
    #       "currencyPairId":"9",
    #       "marketId":"5805"
    #     },
    #     "intervalsUpdate":{
    #       "intervals":[
    #         {
    #           "opentime":"1630886400",
    #           "closetime":"1631145600",
    #           "ohlc":{
    #             "openStr":"51678.7",
    #             "highStr":"52181.73",
    #             "lowStr":"50885.1",
    #             "closeStr":"51617.65"
    #           },
    #           "volumeBaseStr":"41.7458315",
    #           "volumeQuoteStr":"2154780.6992795982",
    #           "periodName":"259200"
    #         },
    #         {
    #           "opentime":"1630540800",
    #           "closetime":"1631145600",
    #           "ohlc":{
    #             "openStr":"48885.23",
    #             "highStr":"52181.73",
    #             "lowStr":"48383.88",
    #             "closeStr":"51617.65"
    #           },
    #           "volumeBaseStr":"239.87955476",
    #           "volumeQuoteStr":"12048774.4656522032",
    #           "periodName":"604800"
    #         },
    #         {
    #           "opentime":"1630886400",
    #           "closetime":"1631491200",
    #           "ohlc":{"openStr":"51678.7","highStr":"52181.73","lowStr":"50885.1","closeStr":"51617.65"},
    #           "volumeBaseStr":"41.7458315",
    #           "volumeQuoteStr":"2154780.6992795982",
    #           "periodName":"604800_Monday"
    #         }
    #       ]
    #     }
    #   }
    # }


  def run(self):
    data_domain = self.URL.replace("https://","")
    endpoint = f"wss://{data_domain}/connect?apikey={self.KEY_ID}"
    ws = websocket.WebSocketApp(endpoint, on_open=self.on_open, on_message=self.on_message)
    ws.run_forever()

  def __repr__(self):
      return f'<CryptowatchStream ()>'
