import abc
import luigi
import time
from nameko.rpc import rpc, RpcProxy
from typing import List
import logging
from isharp.datahub.core import DatahubTarget
logger = logging.getLogger(__name__)



class EvalMethod(object):
    pass

class Evaluator(abc.ABC):
    @abc.abstractmethod
    def eval(self, method:EvalMethod ,inputs: List[DatahubTarget])->List[DatahubTarget]:
        pass



class EvalService(Evaluator):
    name="evaluation_service"

    @rpc
    def eval(self, method: EvalMethod, inputs: List[DatahubTarget]) -> List[DatahubTarget]:
        logger.info("START performing an eval....")
        time.sleep(1)
        logger.info("END performing an eval....")
        return [DatahubTarget(url="url",t=0)]



