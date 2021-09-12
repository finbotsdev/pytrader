# encoding: utf-8

import pytrader.config as cfg
from pytrader.log import logger
import requests
from requests.adapters import HTTPAdapter
from requests.auth import AuthBase
from requests.packages.urllib3.util.retry import Retry
import traceback


class CoinmarketcapPro():

  def __init__(self):
    self.URL = cfg.get('CMC_PRO_API_URL')
    self.VERSION = 'v1'

  def get(self, path, **kwargs):
    params=[]
    for key, value in kwargs.items():
      if value:
        params.append(f"{key}={value}")

    url = f"{self.URL}/{self.VERSION}/{path}"

    if params:
      url = "?".join([url, "&".join(params)])

    auth = CoinmarketcapProAuth()

    s = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[ 500, 502, 503, 504 ])
    s.mount('https://', HTTPAdapter(max_retries=retries))
    r = s.get(url, auth=auth)

    if r.ok:
      return r.json()
    else:
      print(r.status_code, r.reason, url)

  # https://coinmarketcap.com/api/documentation/v1/#tag/blockchain
  # /blockchain/*	Endpoints that return block explorer related data for blockchains.
  # /v1/blockchain/statistics/latest - Latest statistics

  # https://coinmarketcap.com/api/documentation/v1/#tag/cryptocurrency
  # /cryptocurrency/*	Endpoints that return data around cryptocurrencies such as ordered cryptocurrency lists or price and volume data.
  # /v1/cryptocurrency/map - CoinMarketCap ID map
  def get_crypto_map(self):
    return self.get(f"cryptocurrency/map")
  # /v1/cryptocurrency/info - Metadata
  def get_crypto_info(self, symbol):
    return self.get(f"cryptocurrency/info", symbol=symbol)
  # /v1/cryptocurrency/listings/latest - Latest listings
  def get_crypto_listings_latest(self):
    return self.get(f"cryptocurrency/listings/latest")
  # /v1/cryptocurrency/listings/historical - Historical listings
  def get_crypto_listings_historical(self):
    return self.get(f"cryptocurrency/listings/latest")

  # /v1/cryptocurrency/quotes/latest - Latest quotes
  # /v1/cryptocurrency/quotes/historical - Historical quotes
  # /v1/cryptocurrency/market-pairs/latest - Latest market pairs
  # /v1/cryptocurrency/ohlcv/latest - Latest OHLCV
  # /v1/cryptocurrency/ohlcv/historical - Historical OHLCV
  # /v1/cryptocurrency/price-performance-stats/latest - Price performance Stats
  # /v1/cryptocurrency/categories - Categories
  def get_crypto_categories(self):
    return self.get(f"cryptocurrency/categories")
  # /v1/cryptocurrency/category - Category
  # /v1/cryptocurrency/airdrops - Airdrops
  def get_crypto_airdrops(self):
    return self.get(f"cryptocurrency/airdrops")
  # /v1/cryptocurrency/airdrop - Airdrop
  # /v1/cryptocurrency/trending/latest - Trending Latest
  def get_crypto_trending_latest(self):
    return self.get(f"cryptocurrency/trending/latest")
  # /v1/cryptocurrency/trending/most-visited - Trending Most Visited
  # /v1/cryptocurrency/trending/gainers-losers - Trending Gainers & Losers
  def get_crypto_trending_movers(self):
    return self.get(f"cryptocurrency/trending/gainers-losers")

  #  https://coinmarketcap.com/api/documentation/v1/#tag/exchange
  # /exchange/*	Endpoints that return data around cryptocurrency exchanges such as ordered exchange lists and market pair data.
  # /v1/exchange/map - CoinMarketCap ID map
  # /v1/exchange/info - Metadata
  # /v1/exchange/listings/latest - Latest listings
  # /v1/exchange/listings/historical - Historical listings
  # /v1/exchange/quotes/latest - Latest quotes
  # /v1/exchange/quotes/historical - Historical quotes
  # /v1/exchange/market-pairs/latest - Latest market pairs

  # https://coinmarketcap.com/api/documentation/v1/#tag/fiat
  # /fiat/*	Endpoints that return data around fiats currencies including mapping to CMC IDs.
  # /v1/fiat/map - CoinMarketCap ID map

  # https://coinmarketcap.com/api/documentation/v1/#tag/global-metrics
  # /global-metrics/*	Endpoints that return aggregate market data such as global market cap and BTC dominance.
  # /v1/global-metrics/quotes/latest - Latest global metrics
  # /v1/global-metrics/quotes/historical - Historical global metrics

  # https://coinmarketcap.com/api/documentation/v1/#tag/key
  # /key/*	API key administration endpoints to review and manage your usage.
  # /v1/key/info - Key Info

  # https://coinmarketcap.com/api/documentation/v1/#tag/market-pairs
  # /partners/*	Endpoints for convenient access to 3rd party crypto data.
  # /v1/partners/flipside-crypto/fcas/listings/latest - List all available FCAS scores
  # /v1/partners/flipside-crypto/fcas/quotes/latest - Request specific FCAS scores

  # https://coinmarketcap.com/api/documentation/v1/#tag/tools
  # /tools/*	Useful utilities such as cryptocurrency and fiat price conversions.
  # /v1/tools/price-conversion - Price conversion tool


class CoinmarketcapProAuth(AuthBase):

    def __init__(self):
        self.api_key = cfg.get('CMC_PRO_API_KEY')

    def __call__(self, request):
        request.headers.update({
            'X-CMC_PRO_API_KEY': self.api_key,
            'Content-Type': 'application/json'
        })
        return request


