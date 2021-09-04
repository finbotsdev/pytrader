import pytrader as pt
from pytrader.data import IEXCloud
import pytrader.log as log

timer = pt.Timer()

logger = log.logging
log.config_root_logger()

api = IEXCloud('MSFT')

logger.info('get_logo')
print(api.get_logo())

logger.info('get_company_info')
print(api.get_company_info())

logger.info('get_company_news')
print(api.get_company_news())

logger.info('get_stats')
print(api.get_stats())

logger.info('get_fundamentals')
print(api.get_fundamentals())

logger.info('get_dividends')
print(api.get_dividends())

logger.info('get_institutional_ownership')
print(api.get_institutional_ownership())

logger.info('get_insider_transactions')
print(api.get_insider_transactions())

timer.report()
