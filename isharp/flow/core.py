import dataclasses
import isharp.datahub.broker_client
from  isharp.datahub.core import DataBroker
from typing import List
@dataclasses.dataclass(frozen=True)
class DatahubRequirement:
    name:str
    url:str
    t: int


@dataclasses.dataclass(frozen=True)
class CalculationTask:
    requirements: List[DatahubRequirement]
    strategy: str
    dueBy: str
    eval_label: str







