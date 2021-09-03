from pytrader.data import IEXCloud

api = IEXCloud('MSFT')

print(api.get_logo())
print(api.get_company_info())
print(api.get_company_news())
print(api.get_stats())
print(api.get_fundamentals())
print(api.get_dividends())
print(api.get_institutional_ownership())
print(api.get_insider_transactions())
