from isharp.core import StorageMethod,MatrixHeader,Revision,AcquireContentReturnValue,MemStyles
from typing import List
import os



class ArcticStorageMethod(StorageMethod):

    def __init__(self,store):
        self.store = store
        super().__init__("arctic",[])

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

    def acquireContent(self, path, params, version_id=None)->AcquireContentReturnValue:
        self._check_params(params)

        library, ticker = self._lib_ticker(path)
        lib = self.store[library]
        v = None if version_id is None else int(version_id)
        versioned  = lib.read(ticker, v)
        header = MatrixHeader(
        name="",
        revision_id= str(versioned.version),
        storage_method=self.name,
        path= path,
        memory_style=MemStyles.DATA_FRAME,
        description=None
        )


        return AcquireContentReturnValue(content=versioned.data,header=header)




    def storeContent(self, path, params, content,revision_info)->Revision:
        self._check_params(params)
        library, ticker = self._lib_ticker(path)
        lib = self.store[library]
        lib.write(ticker,content )

    def list(self) -> List[MatrixHeader]:
        pass




