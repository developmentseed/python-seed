import luigi
import time
import datetime
from multiprocessing import Process
from isharp.flow.core import CalculationTask
from isharp.flow.neo4jflow.py2neoflow import  calcTasks
from typing import List


class DataHubTarget(luigi.Target):

    def __init__(self,data_hub_requirement) -> None:
        super().__init__()
        self.data_hub_requirement = data_hub_requirement

    def exists(self):
        return self.data_hub_requirement.exists()

class DataHubInput(luigi.ExternalTask):
    task_namespace = "isharp"
    task_family="DataRequirement"

    url = luigi.Parameter()
    t = luigi.IntParameter(significant=False)

    @classmethod
    def get_param_values(cls, params, args, kwargs):
        return super().get_param_values(params, (), kwargs)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data_hub_target=args[0]


    def output(self):
        return self.data_hub_target

class LuigiCalculationTask(luigi.Task):
    accepts_messages = True
    task_namespace = "isharp"
    task_family="StrategyCalculation"
    strategy = luigi.Parameter()
    dueBy = luigi.Parameter()
    eval_label=luigi.Parameter()


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.requirements= args[0]

    @classmethod
    def get_param_values(cls, params, args, kwargs):
        return super().get_param_values(params, (), kwargs)


    def requires(self):
        return self.requirements


def submit(task:CalculationTask):
    luigi.build([task])



if __name__ == '__main__':
    for calc_task in calcTasks():
        inputs = [DataHubInput(i, url=i.url, t=i.t) for i in calc_task.requirements]
        task = LuigiCalculationTask(inputs, strategy=calc_task.strategy, dueBy=calc_task.dueBy, eval_label=calc_task.dueBy)
        p= Process(target=submit, args=(task,))
        p.start()









