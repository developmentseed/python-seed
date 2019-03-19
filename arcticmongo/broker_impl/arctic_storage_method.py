from core.matrix import StorageMethod
import pandas as pd
import os


class ArcticStorageMethod(StorageMethod):

    def __init__(self,store):
        self.store = store
        super().__init__("mongo",[])


    def acquireContent(self, path, params):
        self._check_params(params)
        library, ticker = os.path.split(path)
        if  library in self.store.list_libraries():
            lib = self.store[library]
            if lib.has_symbol(ticker):
                return lib.read(ticker)
            else:
                raise StorageMethod.ResourceException("ticker {} not found".format(ticker))
        else:
            raise StorageMethod.ResourceException("library {} not found".format(library))


    def storeContent(self, path, params, content):
        self._check_params(params)