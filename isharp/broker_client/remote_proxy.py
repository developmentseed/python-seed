from typing import List
from isharp.core import DataBroker, MatrixHeader, Matrix, AcquireContentReturnValue, Revision
from isharp.core import MatrixUrl
from isharp.core import RevisionInfo
from urllib.parse import urlparse
from nameko.standalone.rpc import ClusterRpcProxy
import logging
logger = logging.getLogger(__name__)


def remote_config(net_location:str):
    return {
        'serializer': 'pickle',
        'AMQP_URI': 'pyamqp://guest:guest@{}'.format(net_location),
        'rpc_exchange': 'nameko-rpc',
        'max_workers': 10,
        'parent_calls_tracked': 10
    }

class PooledBrokerConnection(DataBroker):
    def __init__(self, net_location: str):
        logger.info("creating remote client at {}".format(net_location) )
        conf = remote_config(net_location)
        self.rpc_proxy = ClusterRpcProxy(conf)
        self.proxy = self.rpc_proxy.start()
        self.net_location = net_location

    def stop(self):
        logger.info("closing remote client at {}".format(self.net_location))
        self.rpc_proxy.stop()


    def commit(self, matrix: Matrix, revisionInfo: RevisionInfo) -> Revision:
        pass

    def list(self) -> List[MatrixHeader]:
        return self.proxy.data_broker_service.list()

    def checkout(self, url: str, version_id=None) -> Matrix:
        return self.proxy.data_broker_service.checkout(url)


class BrokerConnectionPool(DataBroker):
    def __init__(self):
        self.pool = {}

    def __enter__(self):
        return self

    def  __exit__(self, exc_type, exc_value, traceback):
        for thisConnection in self.pool.values():
            thisConnection.stop()

    def _acquire_connection(self, connection_key):
        if connection_key not in self.pool.keys():
            self.pool[connection_key] = PooledBrokerConnection(connection_key)
        return self.pool[connection_key]

    def _connect(self, url: str):
        connection_key = self._conn_details(url)
        return self._acquire_connection(connection_key)

    def _conn_details(self, url: str) -> str:
        url_components = urlparse(url)
        return  url_components.netloc

    def checkout(self, url: str, version_id=None) -> Matrix:
        return self._connect(url).checkout(url, version_id)

    def commit(self, matrix: Matrix, revisionInfo: RevisionInfo) -> Revision:
        return self._connect(matrix.url.url).commit(matrix, revisionInfo)

    def release(self, matrix) -> None:
        self._connect(matrix.url.url).release(matrix)

    def list(self,network_location):
        return self._acquire_connection(network_location).list()




