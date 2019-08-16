import abc
import luigi
import time
from nameko.rpc import rpc, RpcProxy
from typing import List
import logging
logger = logging.getLogger(__name__)



class EvalMethod(object):
    pass

class Evaluator(abc.ABC):
    @abc.abstractmethod
    def eval(self, method:EvalMethod ,inputs: List[EvalTarget])->List[EvalTarget]:
        pass



class EvalService(Evaluator):
    name="evaluation_service"

    @rpc
    def eval(self, method: EvalMethod, inputs: List[EvalTarget]) -> List[EvalTarget]:
        logger.info("START performing an eval....")
        time.sleep(5)
        logger.info("END performing an eval....")
        return []



