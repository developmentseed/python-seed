import luigi
import time
from multiprocessing import Process
from isharp.flow.core import CalculationTask
from isharp.flow.neo4jflow.py2neoflow import  calcTasks
from isharp.datahub.broker_client.remote_proxy import  BrokerConnectionPool



class DataHubTarget(luigi.Target):
    def __init__(self,data_hub_requirement,data_broker):
        self.data_hub_requirement = data_hub_requirement
        self.data_broker = data_broker

    def exists(self):

        peeked =  self.data_broker.peek(self.data_hub_requirement.url)
        print(" would be checking for url {} -> {}".format(self.data_hub_requirement.url,peeked))
        return peeked != None


class DataHubInputTask(luigi.ExternalTask):
    task_namespace = "isharp"
    task_family="DataRequirement"
    url = luigi.Parameter()
    t = luigi.IntParameter()

    def registerTarget(self,requirement,data_broker):
        self.data_hub_target = DataHubTarget(requirement,data_broker)

    def output(self):
        return self.data_hub_target



class LuigiCalculationTask(luigi.Task):
    accepts_messages = True
    task_namespace = "isharp"
    task_family="StrategyCalculation"
    strategy = luigi.Parameter()
    dueBy = luigi.Parameter()
    eval_label=luigi.Parameter()

    def set_requirements(self,requirements):
        self.requirements = requirements


    def run(self):
        progress = 0
        while True:
            progress += 1
            self.set_progress_percentage(progress)
            self.set_status_message("Doing stage {}".format(progress))
            time.sleep(1)
            print("_____________checking messages for job {} {} ".format(self.strategy,self.dueBy))
            if not self.scheduler_messages.empty():
                msg = self.scheduler_messages.get()
                print ("received {}".format(msg.content))
                if msg.content == "terminate":
                    break
                else:
                    msg.respond("unknown message")
        print ("finished")


    def requires(self):
        return self.requirements


def buildTask(calc_task,data_broker):
    task = LuigiCalculationTask(strategy=calc_task.strategy, dueBy=calc_task.dueBy, eval_label=calc_task.dueBy)
    requirements = []
    for reqiurement in calc_task.requirements:
          input_task = DataHubInputTask(url=reqiurement.url, t=reqiurement.t)
          input_task.registerTarget(reqiurement,data_broker)
          requirements.append(input_task)
    task.set_requirements(requirements)
    return task



def submit(task:CalculationTask):
    luigi.build([task])



if __name__ == '__main__':
    broker = BrokerConnectionPool()
    for calc_task in calcTasks("datahub","5672"):
        task = buildTask(calc_task,broker)
        p= Process(target=submit, args=(task,))
        p.start()









