from nameko.extensions import DependencyProvider
from nameko.rpc import rpc, RpcProxy
from isharp.core import  MatrixHeader,CombiBroker
from typing import List
from isharp.core import  DataBroker,Matrix,RevisionInfo,Revision
import logging

logger = logging.getLogger(__name__)

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
        ret_val = self.delegate.checkout(url,version_id)
        logger.debug("call to delegate successful")
        return ret_val
    @rpc
    def commit(self, matrix: Matrix, revisionInfo: RevisionInfo) -> Revision:
        return super().commit(matrix, revisionInfo)
    @rpc
    def release(self, matrix) -> None:
        pass
    @rpc
    def list(self) -> List[MatrixHeader]:
        pass




