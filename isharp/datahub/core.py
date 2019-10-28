
from enum import Enum
from typing import List
import dataclasses
from urllib.parse import urlparse
from urllib.parse import parse_qsl
import datetime
import abc
import luigi



import logging
logger = logging.getLogger(__name__)



from collections import namedtuple
class MemStyles(Enum):
    DATA_FRAME = 1
    TREE = 2


@dataclasses.dataclass(frozen=True)
class RevisionInfo:
    who: str
    what: str
    when: datetime.datetime





@dataclasses.dataclass(frozen=True)
class Revision:
    id: str
    revision_info: RevisionInfo












class MatrixUrl:
    def __init__(self,url):
        self.url = url
        self.url_components = urlparse(url)
        logger.debug("Parsed Url: host:[{}] path:[{}] port:[{}] scheme:[{}]".format(self.host(),self.path(),self.port(),self.scheme()))

    def params(self):
        params = parse_qsl(self.url_components.query)
        ret_val = {}
        for this_param in params:
            ret_val[this_param[0]] = this_param[1]
        return ret_val

    def host(self):
        return self.url_components.hostname

    def path(self):
        return  self.url_components.path

    def port(self):
        return self.url_components.port

    def scheme(self):
        return self.url_components.scheme


@dataclasses.dataclass(frozen=True)
class MatrixHeader:
    name: str
    revision_id: str
    storage_method: str
    path: str
    memory_style:MemStyles
    description: str

@dataclasses.dataclass(frozen=True)
class MatrixPreview:
    header: MatrixHeader
    range_start: str
    range_end: str


@dataclasses.dataclass(frozen=True)
class Matrix:
    matrix_header: MatrixHeader
    content: object
    url: MatrixUrl

    def replace_content(self,new_content):
        return Matrix(matrix_header=self.matrix_header,url=self.url,content=new_content)



class DataBroker(abc.ABC):

    class CheckoutException(Exception):
        pass

    class ProtocolException(Exception):
        pass

    @abc.abstractmethod
    def checkout(self, url:str, version_id=None)->Matrix:
        pass

    @abc.abstractmethod
    def view(self, url:str, version_id=None)->Matrix:
        pass

    @abc.abstractmethod
    def history(selfurl:str)->List[Revision]:
        pass


    @abc.abstractmethod
    def commit(self,matrix:Matrix,revisionInfo:RevisionInfo)->Revision:
        pass


    def release(self,matrix)->None:
        pass

    @abc.abstractmethod
    def list(self)->List[MatrixHeader]:
        pass


    @abc.abstractmethod
    def peek(self,url)->MatrixPreview:
        pass


    @abc.abstractmethod
    def releaseAll(self)->None:
        pass



AcquireContentReturnValue = namedtuple('AcquireContentReturnValue', 'header content')


class StorageMethod(abc.ABC):
    class ParameterException(Exception):
        pass
    class ResourceException(Exception):
        pass

    def __init__(self, name):
        self.name = name

    @abc.abstractmethod
    def acquireContent(self,path,params,version_id=None)->AcquireContentReturnValue:
        pass


    @abc.abstractmethod
    def storeContent(self,path,params,content,revision_info)->Revision:
        pass


    @abc.abstractmethod
    def list(self)->List[MatrixHeader]:
        pass


class AbstractDataBroker(DataBroker):
    def __init__(self,storage_method):
        super().__init__()
        self.storage_method = storage_method
        self.register = []

    def _assert_not_checked_out(self,matrix_url):
        if matrix_url.path() in self.register:
            raise DataBroker.CheckoutException("matrix [{}] is already checked out".format(matrix_url.path()))

    def _assert_checked_out(self,matrix_url):
        if matrix_url.path() not in self.register:
            raise DataBroker.CheckoutException("matrix [{}] is not already checked out".format(matrix_url.path()))

    def _check_schema(self,matrix_url):
        if matrix_url.scheme() != self.storage_method.name:
            raise DataBroker.ProtocolException()

    def _open(self, matrix_url_str,checkout,version=None ):
        logger.debug("Abstract  broker called with {} checkout ? {}".format(matrix_url_str,checkout))
        matrix_url = MatrixUrl(matrix_url_str)
        self._check_schema(matrix_url)
        if checkout:
            self._assert_not_checked_out(matrix_url)
            self.register.append(matrix_url.path())
        result = self.storage_method.acquireContent(path=matrix_url.path(), params=matrix_url.params(),version_id=version)
        ret_val =Matrix(result.header,result.content,matrix_url)
        logger.debug("Abstract data broker about to return matrix")
        return ret_val

    def checkout(self, matrix_url_str,version=None):
        return self._open(matrix_url_str,True,version)


    def history(self,url: str) -> List[Revision]:
        matrix_url = MatrixUrl(url)
        self._check_schema(matrix_url)
        return self.storage_method.history(matrix_url)

    def view(self, matrix_url_str,version=None):
        return self._open(matrix_url_str, False,version)

    def commit(self, matrix, revisionInfo):
        self._assert_checked_out(matrix.url)
        revision = self.storage_method.storeContent(path=matrix.matrix_header.path,content=matrix.content,revision_info=revisionInfo,params=matrix.url.params())
        self.register.remove(matrix.url.path())
        return revision

    def releaseAll(self):
        logger.debug("Abstract databroker about to release all")
        self.register.clear()

    def release(self, matrix):
        self.register.remove(matrix.url.path())

    def list(self):
        return self.storage_method.list()

    def peek(self, url) -> MatrixPreview:
        matrix_url = MatrixUrl(url)
        self._check_schema(matrix_url)
        try:
            content_tuple = self.storage_method.acquireContent(path=matrix_url.path(), params=matrix_url.params(),version_id=None)
            return  MatrixPreview(header =  content_tuple.header, range_start=content_tuple.content.index[0], range_end=content_tuple.content.index[-1])
        except StorageMethod.ResourceException:
            return None


class CombiBroker(DataBroker):
    def __init__(self,registry):
        self.registry = registry

    def checkout(self, url, version_id=None) -> Matrix:
        logger.info("combi broker called with {}".format(url))
        parsed_url = MatrixUrl(url)
        return self._delegate(parsed_url.scheme()).checkout(url,version_id)

    def history(self ,url:str ) -> List:
        logger.info("combi broker history called with {}",url)
        parsed_url = MatrixUrl(url)
        return self._delegate(parsed_url.scheme()).history(url)

    def view(self, url, version_id=None) -> Matrix:
        logger.info("combi broker View called with {}".format(url))
        parsed_url = MatrixUrl(url)
        return self._delegate(parsed_url.scheme()).view(url,version_id)


    def peek(self, url) -> MatrixHeader:
        logger.info("combi broker called with peek {}".format(url))
        parsed_url = MatrixUrl(url)
        return self._delegate(parsed_url.scheme()).peek(url)

    def _delegate(self,scheme)->DataBroker:
        if (scheme in self.registry):
            return self.registry[scheme]
        else:
            raise DataBroker.ProtocolException("invalid protocol: {}".format(scheme))


    def commit(self, matrix: Matrix, revisionInfo: RevisionInfo) -> Revision:
        logger.info("combi broker  commit called ")
        return self._delegate(matrix.url.scheme()).commit(matrix,revisionInfo)

    def release(self, matrix) -> None:
        logger.info("combi broker  release called")
        self._delegate(matrix.url.scheme()).release(matrix)
        return None

    def releaseAll(self) -> None:
        logger.info("combi broker  release called")
        for broker in self.registry.values():
            broker.releaseAll()

    def list(self) -> List[MatrixHeader]:
        logger.info("combi broker list method called")
        ret_val = []
        for this_delegate in self.registry.values():
            logger.info("getting listing from delegate")
            this_pack = this_delegate.list()
            for listing_item in this_pack:
                ret_val.append(listing_item)

        logger.info("combi broker returning listing with {} values".format(len(ret_val)))
        return ret_val



@dataclasses.dataclass(frozen=True)
class DatahubTarget():
    url: str
    t: int


    def exists(self,data_broker)->bool:
        return data_broker.peek(self.url) != None
