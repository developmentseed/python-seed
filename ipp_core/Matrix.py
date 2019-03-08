import abc
from enum import Enum
import typing
import dataclasses
class Matrix:

    def __init__(self,matrixHeader,content):
        self.matrixHeader = matrixHeader
        self.content = content




class MatrixHeader:
    def __init__(self,revisions,schema,storage_method,url):
        self.revisions = revisions
        self.schema = schema
        self.storage_method = storage_method


class StorageMethod(abc.ABC):
    def __init__(self,params,name):
        self.params = params
        self.name = name

    @abc.abstractmethod
    def acquireContent(self):
        pass


class Schema:
    def __init__(self,axes):
        self.axes = axes


class Axis:
    def __init__(self,axis_type,label,coordinates):
        self.axis_type = axis_type
        self.label = label
        self.coordinates = coordinates

class AxisTypes(Enum):
    TIME_SERIES= 1
    CATEGORY = 2

class Revision:
    def __init__(self,id,revision_info):
        self.id = id
        self.revision_info = revision_info

@dataclasses.dataclass(frozen=True)
class RevisionInfo:
    who: str
    what: str
    when: typing.Any
    def __init__(self, who,when,what):
        self.who = who
        self.what = what
        self.when = typing.Any


