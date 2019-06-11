from nameko.extensions import DependencyProvider
from nameko.rpc import rpc, RpcProxy
from isharp.core import  MatrixHeader,CombiBroker
from typing import List
from isharp.core import  DataBroker,Matrix,RevisionInfo,Revision
from isharp.csv_files.simple_file_broker import SimpleFileBroker
import logging

logger = logging.getLogger(__name__)


def create_yaml_driven_combi_broker(config):
    logger.info("Config for combi broker: {}".format(config))
    file_broker_spec = config.get('file')
    root_directory = file_broker_spec.get('root_directory')
    logger.info("file spec={}".format(root_directory))

    fileBroker =SimpleFileBroker(root_directory)

    return CombiBroker({"file":fileBroker})

class DataBrokerDelegate(DependencyProvider):

    def get_dependency(self, worker_ctx):
        data_brokers =worker_ctx.container.config.get('DATA_BROKERS')
        return create_yaml_driven_combi_broker(data_brokers)


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









