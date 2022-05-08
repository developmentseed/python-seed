import os
from neomodel import config,db
import yaml
from isharp.sakura import sakuragraphmodel

yaml_dir = os.path.dirname(os.path.realpath(__file__))
trading_center_nodes = {}
instrument_nodes = {}
db.set_connection("bolt://neo4j:guest@localhost:7687")

def deleteData():
    print ('Delete all nodes and relationships...')
    query = 'MATCH (n) DETACH DELETE n'
    db.cypher_query(query)


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





def build_instruments_from_yaml(file_name):
    with open(os.path.join(yaml_dir, file_name)) as f:
        instrs = yaml.load(f, Loader=yaml.FullLoader)
        for key, value in instrs.items():
            newNode = sakuragraphmodel.Instrument(code=key, caption = value['caption']).save()
            newNode.tradingCenter.connect(trading_center_nodes[value['tradingCenter']])
            instrument_nodes[key] = newNode
            for  feed_map in value['feeds']:
                for (key,value) in feed_map.items():
                    source_node = sakuragraphmodel.Source(code=key).save()
                    newNode.feed.connect(source_node)
                    for capture in value:
                            for capt_key,capt_list in capture.items():
                                if (capt_list is not None):
                                    for capture_item in capt_list:
                                        source_node.__getattribute__(capt_key).connect(sakuragraphmodel.TimeSeries(name=capture_item).save())




def build_trading_ceters_from_yaml(file_name):
    with open(os.path.join(yaml_dir, file_name)) as f:
        tcs = yaml.load(f, Loader=yaml.FullLoader)
        for key, value in tcs.items():
            trading_center_nodes[key] = sakuragraphmodel.TradingCenter(code=key, tz=value['tz']).save()




deleteData()
build_trading_ceters_from_yaml('tradingcenters.yaml')
build_instruments_from_yaml('instruments.yaml')
build_strategies_from_yaml('strategies.yaml')












