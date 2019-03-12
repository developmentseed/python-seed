import abc
from enum import Enum
import typing
import dataclasses
class Matrix:

    def __init__(self, matrix_header, content):
        self.matrix_header = matrix_header
        self.content = content


class MatrixHeader:
    class MemStyles(Enum):
        DATA_FRAME= 1
        TREE=2

    def __init__(self, name, revisions, storage_method, url, memory_style):
        self.revisions = revisions
        self.storage_method = storage_method
        self.url = url
        self.name = name
        self.memory_style = memory_style


class StorageMethod(abc.ABC):
    class ParameterException(Exception):
        pass
    class ResourceException(Exception):
        pass

    def __init__(self, name, required_params):
        self.required_parameters = required_params
        self.name = name

    @abc.abstractmethod
    def acquireContent(self,path,params):
        pass



class Axis:
    class Types(Enum):
        TIME_SERIES = 1
        CATEGORY = 2
    def __init__(self,label,axis_type):
        self.axis_type = axis_type
        self.label = label


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


