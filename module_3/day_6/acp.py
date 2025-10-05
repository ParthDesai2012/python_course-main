import calendar
from datetime import date
today = date.today()
year = today.year
month = today.month
print(calendar.month(year, month))