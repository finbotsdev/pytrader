# encoding: utf-8

import pytrader.config as cfg
import requests

class IEXCloud:

    def __init__(self, symbol):
        self.URL = cfg.get('IEX_API_DATA_URL')
        self.KEY_ID = cfg.get('IEX_API_KEY_ID')
        self.SECRET_KEY = cfg.get('IEX_API_SECRET_KEY')
        self.VERSION = cfg.get('IEX_API_VERSION')
        self.symbol = symbol


    def _request(self, path, **kwargs):
        paramstring=[f'token={self.KEY_ID}']

        for key, value in kwargs.items():
          paramstring.append(f"{key}={value}")

        url = f"{self.URL}/{self.VERSION}/{path}?{'&'.join(paramstring)}"

        r = requests.get(url)

        if r.ok:
          return r.json()
        else:
          print(r.status_code, r.reason, url)


    def get_logo(self):
        return self._request(f"stock/{self.symbol}/logo")

    def get_company_info(self):
        return self._request(f"stock/{self.symbol}/company")

    def get_company_news(self, last=10):
        return self._request(f"stock/{self.symbol}/news/last/{last}")

    def get_dividends(self, range='5y'):
        return self._request(f"stock/{self.symbol}/dividends/{range}")

    def get_fundamentals(self, period='quarterly', last=4):
        return self._request(f"time-series/fundamentals/{self.symbol}/{period}", last=last)

    def get_insider_transactions(self):
        return self._request(f"stock/{self.symbol}/insider-transactions")

    def get_institutional_ownership(self):
        return self._request(f"stock/{self.symbol}/institutional-ownership")

    def get_stats(self):
        return self._request(f"stock/{self.symbol}/advanced-stats")
