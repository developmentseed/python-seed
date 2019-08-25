
from py2neo import  Graph
from isharp.flow.core import CalculationTask, DatahubRequirement




url = "bolt://ec2-34-205-159-121.compute-1.amazonaws.com:7687"


def calcTasks(data_hub_host_name, data_hub_port):
    ret_val = []
    graph = Graph(url)
    strategies = graph.nodes.match('Strategy')
    for strategy in strategies:
        jobs = graph.match((strategy,), r_type='EVAL_JOB')
        for j in jobs:
            deps = []
            job_node = j.end_node
            dependencies = graph.match((job_node,), r_type="USES")
            for dependency in dependencies:
                datahub_url = "{}://{}:{}/{}".format("arctic",data_hub_host_name,data_hub_port,dependency.end_node['path'])
                deps.append(DatahubRequirement(name=dependency.end_node['name'],t=0,url=datahub_url) )
            ret_val.append(CalculationTask(dueBy=job_node['due_by'],requirements=deps,strategy=strategy['name'],eval_label=job_node['name']))

    return ret_val



