import dataclasses
from typing import Dict
from typing import List

from typing import Type
from typing import Any

from django.db import models
class WigModel(models.Model):
    full_name = models.CharField(max_length=100)


class WigConstituent(models.Model):
    owner = models.ForeignKey(WigModel)







@dataclasses.dataclass(frozen=True)
class ParameterFieldDefn:
    name:str
    caption:str
    description:str
    param_type: Type
    required: bool
    default: Any

@dataclasses.dataclass(frozen=True)
class ParameterField:
    defn: ParameterFieldDefn
    value: Any


@dataclasses.dataclass(frozen=True)
class ParameterSet:
    name: str
    description:str
    content:List[ParameterField]





@dataclasses.dataclass(frozen=True)
class IndexConsituent:
    name:str


@dataclasses.dataclass(frozen=True)
class AlgoIndex:
    name:str
    constituentMeta: List[ParameterFieldDefn]
    indexMeta: List[ParameterFieldDefn]
    constituents:List[IndexConsituent]




