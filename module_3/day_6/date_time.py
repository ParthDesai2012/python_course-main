from datetime import date , time , datetime 
import calendar
today = date.today()
now = datetime.now()
print(calendar.month(1, 1))
print("Today's date is", today)
print("\nCurrent Date and time is", now)
print("\nDate components", today.year , today.month, today.day)