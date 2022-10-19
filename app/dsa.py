from datetime import datetime
import datetime as dt
now = dt.datetime.now()
# a = dt.datetime.now().date()
# print(a)
# dic= {}
# dic[x]='b'

# print(dic)
today = now
# print(today.weekday())
today = dt.datetime.now().weekday()
delta = 6-int(today)
thissunday = dt.datetime.now() + dt.timedelta(days = delta)
# print(thissunday)

thissunday = dt.datetime.now() + dt.timedelta(days =6)
print(type(thissunday))
print(type(thissunday))
a = '20221010'
datetime_result = datetime.strptime(a, "%Y%m%d")
x =thissunday - datetime_result
print(x)
