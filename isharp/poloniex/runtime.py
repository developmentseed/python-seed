import datetime

#MESSAGE_TIMESTAMP = 1389348840  # '2014-01-10 10:14:00'
offset =  datetime.timezone(datetime.timedelta(hours=0))

now = datetime.datetime.now(offset)

format = "%Y-%m-%dT%H:%M:%S.%f %Z"
#format datetime using strftime()


print (now.strftime(format))






