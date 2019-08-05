import luigi

from isharp.flow.core import  DatahubRequirement
from isharp.flow.core import CalculationTask
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
    task_namespace = "isharp"
    task_family="StrategyCalculation"
    strategy = luigi.Parameter()
    dueBy = luigi.Parameter()
    eval_label=luigi.Parameter()


    def run(self):
        print("_____________running__________________")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.requirements= args[0]

    @classmethod
    def get_param_values(cls, params, args, kwargs):
        return super().get_param_values(params, (), kwargs)


    def requires(self):
        return self.requirements


def submit(calc_task:CalculationTask):
    inputs = [DataHubInput(i,url=i.url,t=i.t) for i in calc_task.requirements]
    task = LuigiCalculationTask(inputs,strategy=calc_task.strategy, dueBy=calc_task.dueBy, eval_label=calc_task.dueBy)
    luigi.build([task])





if __name__ == '__main__':
    reqs = [DatahubRequirement("USD", "svn:a//", 1),
            DatahubRequirement("JPY", "svn:b//", 2),
            DatahubRequirement("EUR", "svn:c//", 3)]

    task = CalculationTask(strategy="buildtrat", dueBy="0525", eval_label="eodJob",requirements=reqs)

    submit(task)









