from neomodel import config, StructuredNode, StringProperty, IntegerProperty,DateProperty, FloatProperty,DateTimeProperty, RelationshipTo

class Calendar(StructuredNode):
    name = StringProperty(default="CALENDAR")
    next = RelationshipTo(StructuredNode,"NEXT")



class Date(StructuredNode):
    caption=StringProperty(required=True)
    date = DateProperty(required=True)
    next = RelationshipTo(StructuredNode,"NEXT")


class WeekDay(StructuredNode):
    next = RelationshipTo(StructuredNode,'NEXT')
    calendar_date = RelationshipTo(Date,'ON')

class Row(StructuredNode):
    value= FloatProperty(required=True)
    next = RelationshipTo(StructuredNode,"NEXT")
    on = RelationshipTo(WeekDay,"ON")

class Revision(StructuredNode):
    version = StringProperty(required=True)
    timestamp = DateTimeProperty(required=True)
    comment = StringProperty(required=True)
    userId = StringProperty(required=True)
    capture = RelationshipTo(Row, 'CAPTURE')
    backload = RelationshipTo(Row,'BACKLOAD')
    correction = RelationshipTo(Row,'CORRECTION')
    next = RelationshipTo(StructuredNode,'NEXT')



class BizDay(WeekDay):
    pass

class Holiday(WeekDay):
    pass

class TradingCenter(StructuredNode):
    code = StringProperty(unique_index=True, required=True)
    tz = StringProperty(required=True)
    next = RelationshipTo(WeekDay,'NEXT')




class Matrix(StructuredNode):
    name=StringProperty(unique_index=True)


class Market(Matrix):
    pass


class TimeSeries(Matrix):
    next = RelationshipTo(Revision,'NEXT')




class Source(StructuredNode):
    code = StringProperty(required=True)
    EOD = RelationshipTo(TimeSeries,'EOD')
    twap=RelationshipTo(TimeSeries,'TWAP')
    snap=RelationshipTo(TimeSeries,'SNAP')


class InstrumentStaticData(StructuredNode):
    code = StringProperty(unique_index=True, required=True)
    bbg_ticker= StringProperty(required=True)


class Instrument(StructuredNode):
    code = StringProperty(unique_index=True, required=True)
    caption = StringProperty(required=True)
    tradingCenter = RelationshipTo(TradingCenter,'TRADES_ON')
    feed = RelationshipTo(Source,'FEED')



class Task(StructuredNode):
    name=StringProperty(unique_index=False,required=True)
    nextTask = RelationshipTo(StructuredNode,"next")
    requires = RelationshipTo(StructuredNode,"requires")
    produces = RelationshipTo(StructuredNode,"produces")


class WorkPhase(StructuredNode):
    name = StringProperty(unique_index=False, required=True)
    tasks = RelationshipTo(Task, "task")
    nextPhase = RelationshipTo(StructuredNode,"next")



class Workflow(StructuredNode):
    name=StringProperty(unique_index=False,required=True )
    workphase =RelationshipTo(WorkPhase,'next')



class DailySchedule(StructuredNode):
    name=StringProperty(required='True')
    workflow = RelationshipTo(Workflow,'workflow')


class Strategy(StructuredNode):
    name = StringProperty(unique_index=True, required=True)
    component = RelationshipTo(Instrument,"UsesComponent")
    dailySchedule = RelationshipTo(DailySchedule,'schedule')


