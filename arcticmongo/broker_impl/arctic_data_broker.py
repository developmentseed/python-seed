from core.data_broker import DataBroker
import urllib.parse
from core.matrix import Matrix
from ishrp_core.broker_impl.abstract_data_broker import AbstractDataBroker
from .arctic_storage_method import ArcticStorageMethod
class ArcticBroker(AbstractDataBroker):
    def __init__(self,store):
        super().__init__(ArcticStorageMethod(store),"arctic")

    def checkout(self, url):
        return super().checkout(url)

    def commit(self, matrix, revisionInfo):
        super().commit(matrix, revisionInfo)

    def catalogue(self):
        super().catalogue()
        raise Exception("not supported")

