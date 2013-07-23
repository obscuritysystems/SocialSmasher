import datetime
import os
from datetime import timedelta, tzinfo

os.environ['TZ'] = 'America/Denver'
format = "%Y-%m-%dT%H:%M:%S"

today = datetime.datetime.today()
print 'ISO     :', today

s = today.strftime(format)
print 'strftime:', s

d = datetime.datetime.strptime(s, format)
print 'strptime:', d.strftime(format)
