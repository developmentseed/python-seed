from isharp.datahub.core import DataBroker,Matrix,AbstractDataBroker,DirectoryNode
from .arctic_storage_method import ArcticStorageMethod
class ArcticBroker(AbstractDataBroker):
    def __init__(self,store):
        super().__init__(ArcticStorageMethod(store))

    def checkout(self, url,version=None):
        return super().checkout(url,version)

    def commit(self, matrix, revisionInfo):
        super().commit(matrix, revisionInfo)

    def dir(self, path) -> DirectoryNode:
        ret_val=  super().dir(path)
        return ret_val
















