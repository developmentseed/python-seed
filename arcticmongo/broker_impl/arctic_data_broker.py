from core.data_broker import DataBroker
import urllib.parse
from core.matrix import Matrix
from .arctic_storage_method import ArcticStorageMethod
class ArcticBroker(DataBroker):
    def __init__(self,store):
        self.storage_method = ArcticStorageMethod(store)
        super().__init__()

    def checkout(self, url):
        super().checkout(url)


    def commit(self, matrix, revisionInfo):
        super().commit(matrix, revisionInfo)
        raise Exception("not supported")

    def catalogue(self):
        super().catalogue()
        raise Exception("not supported")

