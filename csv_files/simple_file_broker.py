from core.data_broker import DataBroker
import urllib.parse
from core.matrix import Matrix
from core.matrix import MatrixHeader
from .file_storage_method import FileStorageMethod
class SimpleFileBroker(DataBroker):
    file_scheme = "file"
    def __init__(self,root_directory):
        super().__init__()
        self.storage_method = FileStorageMethod(root_directory)

    def checkout(self, url):
        super().checkout(url)
        url_components = urllib.parse.urlparse(url)
        if url_components.scheme == SimpleFileBroker.file_scheme:
            content = self.storage_method.acquireContent(path=url_components.path, params=urllib.parse.parse_qs(url_components.query))
            header = MatrixHeader(url = url,
                                  name=url_components.path,
                                  revisions = [],
                                  storage_method=SimpleFileBroker.file_scheme,
                                  memory_style=MatrixHeader.MemStyles.DATA_FRAME)
            return Matrix(header,content)

        else:
            raise DataBroker.ProtocolException("unknown protocol: {}".format(url_components.scheme))

    def commit(self, matrix,revision_info):
        super().commit(matrix,revision_info)
        url_components = urllib.parse.urlparse(matrix.matrix_header.url)
        self.storage_method.storeContent(path=url_components.path,params=urllib.parse.parse_qs(url_components.query),content=matrix.content)

    def revisions(self, url):
        raise RuntimeError()

    def catalogue(self):
        return self.matrix_headers




