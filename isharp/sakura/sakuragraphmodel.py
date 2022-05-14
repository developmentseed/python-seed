from neomodel import config, StructuredNode, StringProperty, IntegerProperty,DateProperty, FloatProperty,DateTimeProperty, RelationshipTo

class Calendar(StructuredNode):
    next = RelationshipTo(StructuredNode,"NEXT")



class Date(StructuredNode):
    date = DateProperty(required=True)
    next = RelationshipTo(StructuredNode,"NEXT")



class Row(StructuredNode):
    date = DateProperty(required=True)
    value= FloatProperty(required=True)
    next = RelationshipTo(StructuredNode,"NEXT")

class Revision(StructuredNode):
    version = StringProperty(required=True)
    timestamp = DateTimeProperty(required=True)
    capture = RelationshipTo(Row, 'CAPTURE')
    backload = RelationshipTo(Row,'BACKLOAD')
    correction = RelationshipTo(Row,'CORRECTION')
    next = RelationshipTo(StructuredNode,'NEXT')


class TradingCenter(StructuredNode):
    code = StringProperty(unique_index=True, required=True)
    tz = StringProperty(required=True)


class Matrix(StructuredNode):
    name=StringProperty(unique_index=True)




class TimeSeries(Matrix):
    history = RelationshipTo(Revision,'HISTORY')




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


