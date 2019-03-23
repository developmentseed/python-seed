from core.matrix import StorageMethod,MatrixHeader
import pandas as pd
import os



class ArcticStorageMethod(StorageMethod):

    def __init__(self,store):
        self.store = store
        super().__init__("mongo",[])

    def _lib_ticker(self,path):
        library, ticker = os.path.split(path)
        library = library.replace("/", "", 1)
        if  library in self.store.list_libraries():
            lib = self.store[library]
            if lib.has_symbol(ticker):
                versioned  = lib.read(ticker)
                return (library,ticker)

            else:
                raise StorageMethod.ResourceException("ticker {} not found".format(ticker))
        else:
            raise StorageMethod.ResourceException("library {} not found".format(library))

        return (library, ticker)

    def acquireContent(self, path, params, version_id=None):
        self._check_params(params)

        library, ticker = self._lib_ticker(path)
        lib = self.store[library]
        v = None if version_id is None else int(version_id)
        versioned  = lib.read(ticker, v)
        return (versioned.data,MatrixHeader.MemStyles.DATA_FRAME,str(versioned.version))


    def storeContent(self, path, params, content,revision_info):
        self._check_params(params)
        library, ticker = self._lib_ticker(path)
        lib = self.store[library]
        lib.write(ticker,content )


