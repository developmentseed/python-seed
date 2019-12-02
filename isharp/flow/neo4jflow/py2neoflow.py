
from py2neo import  Graph
from isharp.flow.core import CalculationTask, DatahubRequirement
import os




def calcTasks(data_hub_host_name, data_hub_port,  graph_host):

    url = "bolt://{}:7687".format(graph_host)
    print ('................using graph host {}'.format(graph_host) )
    print('.................    using datahub host {}'.format(data_hub_host_name))
    ret_val = []
    graph = Graph(url)
    strategies = graph.nodes.match('Strategy')
    for strategy in strategies:
        jobs = graph.match((strategy,), r_type='EVAL')
        for j in jobs:
            deps = []
            job_node = j.end_node
            dependencies = graph.match((job_node,), r_type="USES")
            for dependency in dependencies:
                datahub_url = "{}://{}:{}/{}".format("arctic",data_hub_host_name,data_hub_port,dependency.end_node['path'])
                deps.append(DatahubRequirement(name=dependency.end_node['name'],t=0,url=datahub_url) )
            ret_val.append(CalculationTask(dueBy=job_node['due_by'],requirements=deps,strategy=strategy['name'],eval_label=job_node['name']))

    return ret_val



