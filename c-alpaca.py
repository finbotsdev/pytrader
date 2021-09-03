from pytrader.data import AlpacaMarkets, date

api = AlpacaMarkets()

print('get_account', api.get_account())
print('get_assets', api.get_assets())
print('get_calendar', api.get_calendar(end=date('yesterday'), start=date('one week ago')))
print('get_clock', api.get_clock())
print('get_watchlists', api.get_watchlists())
print('get_bars', api.get_bars('AAPL', end=date('yesterday'), start=date('one week ago')))
