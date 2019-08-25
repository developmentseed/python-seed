from typing import List
from nameko.standalone.rpc import ClusterRpcProxy
import logging
import time
from isharp.evalengine.core import Evaluator,EvalMethod
from isharp.datahub.core import  DatahubTarget
logger = logging.getLogger(__name__)

def remote_config(net_location: str):
    return {
        'serializer': 'pickle',
        'AMQP_URI': 'pyamqp://guest:guest@{}'.format(net_location),
        'rpc_exchange': 'nameko-rpc',
        'max_workers': 10,
        'parent_calls_tracked': 10
    }

class AsyncEvalServiceInvoker:
    def __init__(self, conf):
        self.rpc_proxy = ClusterRpcProxy(conf)
        self.proxy = self.rpc_proxy.start()

    def eval(self, method: EvalMethod, inputs: List[DatahubTarget]) -> List[DatahubTarget]:
        result = self.proxy.evaluation_service.eval(method, inputs)
        print (result)




    def stop(self):
        self.rpc_proxy.stop()





invoker = AsyncEvalServiceInvoker(remote_config("localhost"))

invoker.eval(None,[])