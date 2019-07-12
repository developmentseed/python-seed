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
        ret_val = []
        for this_lib_name in self.store.list_libraries():
            library = self.store[this_lib_name]
            for this_symbol in library.list_symbols():
                versions = library.list_versions(this_symbol)
                filtered = [version for version in versions if not version['deleted']]
                max_version = max(map(lambda v: v['version'], filtered))
                ret_val.append(MatrixHeader(name=this_symbol,
                                            description="don't know yet",
                                            storage_method = self.name,
                                            memory_style = MemStyles.DATA_FRAME,
                                            revision_id = str(max_version),
                                            path="{}/{}".format(this_lib_name,this_symbol)))

        return ret_val










