from nameko.extensions import DependencyProvider
from nameko.rpc import rpc, RpcProxy
from isharp.datahub.core import  MatrixHeader,CombiBroker
from typing import List
from isharp.datahub.core import  DataBroker,Matrix,RevisionInfo,Revision
import logging


handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(handler)

class DataBrokerDelegate(DependencyProvider):

    def get_dependency(self, worker_ctx):
        print("getting data broker delegates")
        data_brokers =worker_ctx.container.config.get('data_brokers')
        print("got {} data brokers".format(len(data_brokers)))
        return  CombiBroker(data_brokers)

class DataBrokerService(DataBroker):
    name="data_broker_service"
    data_broker_rpc = RpcProxy("data_broker")
    delegate = DataBrokerDelegate()

    @rpc
    def checkout(self, url: str, version_id=None) -> Matrix:
        logger.debug("delegate received checkout call")
        ret_val = self.delegate.checkout(url,version_id)
        logger.debug("checkout call to delegate successful")
        return ret_val

    @rpc
    def view(self, url: str, version_id=None) -> Matrix:
        logger.debug("delegate received view call")
        ret_val = self.delegate.view(url,version_id)
        logger.debug("view call to delegate successful")
        return ret_val

    @rpc
    def commit(self, matrix: Matrix, revisionInfo: RevisionInfo) -> Revision:
        logger.debug("delegate received commit call")
        return super().commit(matrix, revisionInfo)
    @rpc
    def release(self, matrix) -> None:
        logger.debug("delegate received release call")
        self.delegate.release(matrix)
        logger.debug("release call to delegate successful")
        return None

    @rpc
    def releaseAll(self) -> None:
        logger.debug("delegate reeived release all call")
        self.delegate.releaseAll()
        logger.debug("release call to delegate successful")
        return None

    @rpc
    def list(self) -> List[MatrixHeader]:
        logger.debug("delegate about to retrieve listing")
        return self.delegate.list()

    @rpc
    def peek(self, url) -> MatrixHeader:
        logger.debug("delegate about to peek")
        return self.delegate.peek(url)

    @rpc
    def history(self,url: str) -> List[Revision]:
        logger.debug("delegate history call")
        return self.delegate.history(url)









