import os
import datetime
from neomodel import config,db
import yaml
from isharp.sakura import sakuragraphmodel
import QuantLib as ql
import numpy as np
import pandas as pd


# This script will DELETE the contents of the existing neo4j server that is  pointed to
# and and populate it with the instruments, strategies and trading centers that you will
# find in the three yaml files in the same directory.
#
# Please run with the following environmental values:
#
#     NEO4J_USERNAME =<user>
#     NEO4J_PASSWORD =<password>
#     NEO4J_BOLT_URL=bolt: //localhost: 7687
#
#
from isharp.sakura.randomwalk import randomwalk1D

series = pd.date_range(start='2022-05-03', end='2022-06-07', freq='D')
trading_calendars = [['TOK', 'Japan/Tokyo', ql.Japan(), []],
                     ['LON', 'Europe/London', ql.UnitedKingdom(), []],
                     ['CMG', 'US/New York', ql.UnitedStates(), []]
                     ]

yaml_dir = os.path.dirname(os.path.realpath(__file__))

trading_center_nodes = {}
instrument_nodes = {}

bolt_url = "bolt://{}:{}@localhost:7687".format(os.getenv('NEO4J_USERNAME'),os.getenv('NEO4J_PASSWORD'))

db.set_connection(bolt_url)

def deleteData():
    print ('Delete all nodes and relationships...')
    query = 'MATCH (n) DETACH DELETE n'
    db.cypher_query(query)


def find_mkt_data_point(mkt_data_key, mkt_data_path):
    instrument_node = sakuragraphmodel.Instrument.nodes.get(code= mkt_data_key)
    feed_node = instrument_node.feed.search(code=mkt_data_path[0])
    if mkt_data_path[1] =='EOD':
        return feed_node[0].EOD.all()[0]
    else:
        return None

    pass


def find_trading_calendar(calendar_code):
    return next(obj for obj in trading_calendars if obj[0]==calendar_code)

def build_strategies_from_yaml(file_name):
    with open(os.path.join(yaml_dir, file_name)) as f:
        strats = yaml.load(f, Loader=yaml.FullLoader)
        for strat_key, strat_value in strats.items():
            strat_node = sakuragraphmodel.Strategy(name=strat_key).save()
            component_list = strat_value['components']
            for component in component_list:
                strat_node.component.connect(instrument_nodes[component])

            daily_sched_node = sakuragraphmodel.DailySchedule(name="Diary").save()
            strat_node.dailySchedule.connect(daily_sched_node)

            for wkflow_key, wkflow_value in strat_value['workflows'].items():
                workflow_node = sakuragraphmodel.Workflow(name=wkflow_key).save()
                daily_sched_node.workflow.connect(workflow_node)
                work_phase_list = []
                for wkflow_phase_key, wkflow_phase_value in wkflow_value['workphases'].items():
                    work_phase_node = sakuragraphmodel.WorkPhase(name=wkflow_phase_key).save()
                    if (work_phase_list):
                        work_phase_list[-1].nextPhase.connect(work_phase_node)
                    else:
                        workflow_node.workphase.connect(work_phase_node)
                    work_phase_list.append(work_phase_node)

                    for task_key,task_value in wkflow_phase_value['tasks'].items():
                        task_node = sakuragraphmodel.Task(name=task_key).save()
                        work_phase_node.tasks.connect(task_node)
                        #find the mkt_data dependencies                         
                        if task_value['requires'] is not None:
                            for mkt_data_key, market_data_value in task_value['requires']['mkt_data'].items():
                                data_point = find_mkt_data_point(mkt_data_key,market_data_value['path'])
                                if data_point is not None:
                                    task_node.requires.connect(data_point)





def build_instruments_from_yaml(file_name):
    with open(os.path.join(yaml_dir, file_name)) as f:
        instrs = yaml.load(f, Loader=yaml.FullLoader)
        for key, value in instrs.items():
            newNode = sakuragraphmodel.Instrument(code=key, caption = value['caption']).save()
            trading_center_code = value['tradingCenter']
            newNode.tradingCenter.connect(trading_center_nodes[trading_center_code])
            instrument_nodes[key] = newNode
            for  feed_map in value['feeds']:
                for (key,value) in feed_map.items():
                    source_node = sakuragraphmodel.Source(code=key).save()
                    newNode.feed.connect(source_node)
                    for capture in value:
                            for capt_key,capt_list in capture.items():
                                if (capt_list is not None):
                                    for capture_item in capt_list:
                                        time_series = sakuragraphmodel.TimeSeries(name=capture_item).save()
                                        source_node.__getattribute__(capt_key).connect(time_series)
                                        #iterate through trading days for this trading center
                                        trading_days = find_trading_calendar(trading_center_code)[3]

                                        previous_rev = time_series
                                        for idx,trading_day in enumerate(trading_days):
                                            if trading_day.__class__.__name__=='BizDay':
                                                this_revision = sakuragraphmodel.Revision(version=idx,timestamp = datetime.datetime.now(),comment="added by auto loader", userId="loader").save()
                                                previous_rev.next.connect(this_revision)
                                                previous_rev = this_revision
                                                row_node = sakuragraphmodel.Row(value=0.89).save()
                                                this_revision.capture.connect(row_node)
                                                row_node.on.connect(trading_day)











def build_trading_ceters_from_yaml(file_name):
    with open(os.path.join(yaml_dir, file_name)) as f:
        tcs = yaml.load(f, Loader=yaml.FullLoader)
        for key, value in tcs.items():
            trading_center_nodes[key] = sakuragraphmodel.TradingCenter(code=key, tz=value['tz']).save()



def build_calendar():


    calendar_date_nodes = []
    calendar_node = sakuragraphmodel.Calendar().save()


    for idx,d in enumerate(series):
        current_date_node = sakuragraphmodel.Date(date=series[idx], caption=d.strftime('%a%d%b%y')).save()
        calendar_date_nodes.append(current_date_node)
        if idx==0:
            calendar_node.next.connect(current_date_node)
        else:
            calendar_date_nodes[idx-1].next.connect(current_date_node)

        ql_date = ql.Date(d.day, d.month, d.year)


        for trading_calendar in trading_calendars:

            is_weekend = trading_calendar[2].isWeekend(ql_date.weekday())
            if is_weekend:
                continue
            if idx==0:
                trading_center_node = sakuragraphmodel.TradingCenter(code=trading_calendar[0],tz=trading_calendar[1]).save()
                trading_center_nodes[trading_calendar[0]]=trading_center_node
            is_busday = trading_calendar[2].isBusinessDay(ql_date)
            bus_day_node = sakuragraphmodel.BizDay().save() if is_busday else sakuragraphmodel.Holiday().save()
            if len(trading_calendar[3])==0:
                trading_center_node.next.connect(bus_day_node)
            else:
                trading_calendar[3][-1].next.connect(bus_day_node)

            bus_day_node.calendar_date.connect(calendar_date_nodes[idx])
            trading_calendar[3].append(bus_day_node)





deleteData()
build_calendar()
# build_trading_ceters_from_yaml('tradingcenters.yaml')
build_instruments_from_yaml('instruments.yaml')
# build_strategies_from_yaml('strategies.yaml')












