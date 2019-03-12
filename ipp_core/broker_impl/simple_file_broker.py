from ..data_broker import DataBroker
import urllib.parse
from ..matrix import Matrix
from ..matrix import MatrixHeader
from ..broker_impl.file_storage_method import FileStorageMethod
class SimpleFileBroker(DataBroker):
    file_scheme = "file"
    def __init__(self,root_directory):

        self.storage_method = FileStorageMethod(root_directory)


    def checkout(self, url):
        url_components = urllib.parse.urlparse(url)

        if url_components.scheme == SimpleFileBroker.file_scheme:
            xarray = self.storage_method.acquireContent(path=url_components.path, params=urllib.parse.parse_qs(url_components.query))
            header = MatrixHeader(url = url,
                                  name=url_components.path,
                                  revisions = [],
                                  storage_method=SimpleFileBroker.file_scheme,
                                  memory_style=MatrixHeader.MemStyles.DATA_FRAME)
            return Matrix(header,xarray.to_dataframe())

        else:
            raise DataBroker.ProtocolException("unknown protocol: {}".format(url_components.scheme))

    def commit(self, matrix,revision_info):
        raise RuntimeError()

    def revisions(self, url):
        raise RuntimeError()

    def catalogue(self):
        return self.matrix_headers




