import luigi
import time
import datetime
from multiprocessing import Process
from isharp.flow.core import CalculationTask
from isharp.flow.neo4jflow.py2neoflow import  calcTasks
from typing import List

from luigi import rpc


def getRemoteScheduler():
    return rpc.RemoteScheduler("http://localhost:8082")



if __name__ == '__main__':
    sch = getRemoteScheduler()
    workers = sch.worker_list()
    tasks = sch.task_list()
    gr = sch.graph()
    print (gr)
    print(workers)
    for (taskKey,taskValue) in tasks.items():
        print(taskValue)















