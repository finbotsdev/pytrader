import os
import requests

class AlpacaMarkets():

    def __init__(self):
        self.BASE_URL = os.environ.get('APCA_API_BASE_URL')
        self.DATA_URL = os.environ.get('APCA_API_DATA_URL')
        self.KEY_ID = os.environ.get('APCA_API_KEY_ID')
        self.SECRET_KEY = os.environ.get('APCA_API_SECRET_KEY')
        self.VERSION = os.environ.get('APCA_API_VERSION')

        self.auth_header = {
          "APCA-API-KEY-ID": self.KEY_ID,
          "APCA-API-SECRET-KEY": self.SECRET_KEY
        }


    def get(self, path, **kwargs):
        params=[]
        for key, value in kwargs.items():
          params.append(f"{key}={value}")

        url = f"{self.BASE_URL}/{self.VERSION}/{path}"

        if params:
          url = "?".join([url, "&".join(params)])

        r = requests.get(url, headers=self.auth_header)

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

        r = requests.get(url, headers=self.auth_header)

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
      return self.get_data(f"stocks/{symbol}/bars", start=start, end=end, timeframe=timeframe, limit=limit, page_token=page_token, adjustment=adjustment)
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

