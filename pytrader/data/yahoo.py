import yfinance as yf
import logging

logger = logging.getLogger()


class YahooFinance():

  def __init__(self, symbol: str = None):
    if symbol:
      self.set_symbol(symbol)

  def set_symbol(self, symbol):
    self.symbol = symbol

  def actions(self):
      return self.ticker().actions

  def balance_sheet(self):
      return self.ticker().balance_sheet

  def calendar(self):
      return self.ticker().calendar

  def cashflow(self):
      return self.ticker().cashflow

  def earnings(self):
      return self.ticker().earnings

  def dividends(self):
      return self.ticker().dividends

  def financials(self):
      return self.ticker().financials

  def history(self, period: str = "1mo", interval: str = "1d", start: str = None,
      end: str= None, prepost: bool = False, actions: bool = True, auto_adjust: bool = True,
      back_adjust: bool = False, proxy: bool = None, rounding: bool = False, tz = None, **kwargs):
      """
      :Parameters:
          period : str
              Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
              Either Use period parameter or use start and end
          interval : str
              Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
              Intraday data cannot extend last 60 days
          start: str
              Download start date string (YYYY-MM-DD) or _datetime.
              Default is 1900-01-01
          end: str
              Download end date string (YYYY-MM-DD) or _datetime.
              Default is now
          prepost : bool
              Include Pre and Post market data in results?
              Default is False
          auto_adjust: bool
              Adjust all OHLC automatically? Default is True
          back_adjust: bool
              Back-adjusted data to mimic true historical prices
          proxy: str
              Optional. Proxy server URL scheme. Default is None
          rounding: bool
              Round values to 2 decimal places?
              Optional. Default is False = precision suggested by Yahoo!
          tz: str
              Optional timezone locale for dates.
              (default data is returned as non-localized dates)
          **kwargs: dict
              debug: bool
                  Optional. If passed as False, will suppress
                  error message printing to console.
      """
      logger.debug("history called with {} {} {} {} {}".format(self.symbol, period, interval, start, end))
      df = self.ticker().history(period, interval, start,  end, prepost, actions, auto_adjust,
          back_adjust, proxy, rounding, tz, **kwargs)
      logger.info("{} {} bars fetched".format(len(df), interval))
      return df

  def info(self):
      """
      returns:
      {
      'quoteType': 'EQUITY',
      'quoteSourceName': 'Nasdaq Real Time Price',
      'currency': 'USD',
      'shortName': 'Microsoft Corporation',
      'exchangeTimezoneName': 'America/New_York',
      ...
      'symbol': 'MSFT'
      }
      """
      return self.ticker().info

  def isin(self):
      return self.ticker().isin

  def institutional_holders(self):
      return self.ticker().institutional_holders

  def major_holders(self):
      return self.ticker().major_holders

  def options(self):
      return self.ticker().options

  def quarterly_balance_sheet(self):
      return self.ticker().quarterly_balance_sheet

  def quarterly_cashflow(self):
      return self.ticker().quarterly_cashflow

  def quarterly_earnings(self):
      return self.ticker().quarterly_earnings

  def quarterly_financials(self):
      return self.ticker().quarterly_financials

  def recommendations(self):
      return self.ticker().recommendations

  def sustainability(self):
      return self.ticker().sustainability

  def ticker(self):
      """
      returns: yfinance.Ticker object <MSFT>
      """
      return yf.Ticker(self.symbol)
