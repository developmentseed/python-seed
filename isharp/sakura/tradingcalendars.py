import QuantLib as ql
import pandas as pd

series = pd.date_range(start='2022-05-01', end='2022-06-30', freq='D')


calendar_1 = ql.Japan()
mydate = ql.Date(1, ql.May, 2017)


calendar_1.isBusinessDay(mydate)





for d in series:

    ql_date = ql.Date(d.day,d.month,d.year)
    print('{} {} {}'.format(d,calendar_1.isBusinessDay(ql_date),calendar_1.isWeekend(ql_date.weekday())))







