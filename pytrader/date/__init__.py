from datetime import datetime
import parsedatetime

def date(when: str) -> tuple:
  """
  date
  ----------------------
  :param when: str - a relative date expressed as a natural language string
  returns
    a date in string formated '%Y-%m-%d'
    a datetime object
  """
  if when == '':
      return None
  cal = parsedatetime.Calendar()
  time_struct, parse_status = cal.parse(when)
  dt = datetime(*time_struct[:6])
  return dt.strftime('%Y-%m-%d'), dt
