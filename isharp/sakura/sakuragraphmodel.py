from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
    UniqueIdProperty, RelationshipTo)


class TradingCenter(StructuredNode):
    code = StringProperty(unique_index=True, required=True)
    tz = StringProperty(required=True)


class Matrix(StructuredNode):
    name=StringProperty(unique_index=True)

class TimeSeries(Matrix):
    pass


class Source(StructuredNode):
    code = StringProperty()
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


