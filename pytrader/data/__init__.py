from .alpaca import AlpacaMarkets
from .iex import IEXCloud

from datetime import datetime
import parsedatetime

def date(when: str) -> str:
    if when == '':
        return None
    cal = parsedatetime.Calendar()
    time_struct, parse_status = cal.parse(when)
    return datetime(*time_struct[:6]).strftime('%Y-%m-%d')
