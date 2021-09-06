from .alpaca import AlpacaMarkets
from .iex import IEXCloud
from .yahoo import YahooFinance
from datetime import datetime
import parsedatetime

def date(when: str) -> str:
    if when == '':
        return None
    cal = parsedatetime.Calendar()
    time_struct, parse_status = cal.parse(when)
    dt = datetime(*time_struct[:6])
    return dt.strftime('%Y-%m-%d'), dt
