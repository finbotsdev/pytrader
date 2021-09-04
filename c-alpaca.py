import pytrader as pt
from pytrader.data import AlpacaMarkets, date
import pytrader.log as log

timer = pt.Timer()

logger = log.logging
log.config_root_logger()

api = AlpacaMarkets()

logger.info('get_account')
print(api.get_account())

logger.info('get_assets')
print(api.get_assets())

logger.info('get_calendar')
print(api.get_calendar(end=date('yesterday'), start=date('one week ago')))

logger.info('get_clock')
print(api.get_clock())

logger.info('get_watchlists')
print(api.get_watchlists())

logger.info('get_bars')
print(api.get_bars('AAPL', end=date('yesterday'), start=date('one week ago')))

timer.report()
