import urllib.parse
from core.matrix import MatrixHeader,Matrix
from core.data_broker import DataBroker
class AbstractDataBroker(DataBroker):

    def __init__(self,storage_method,scheme):
        super().__init__()
        self.storage_method = storage_method
        self.scheme=scheme
        self.register = []

    def _assert_not_checked_out(self,url):
        if url in self.register:
            raise DataBroker.CheckoutException("matrix [{}] is already checked out".format(url))

    def _assert_checked_out(self,url):
        if url not in self.register:
            raise DataBroker.CheckoutException("matrix [{}] is not already checked out".format(url))

    def checkout(self, url,version=None):
        self._assert_not_checked_out(url)
        url_components = urllib.parse.urlparse(url)
        if url_components.scheme == self.scheme:
            (content, memory_style,revision_id) = self.storage_method.acquireContent(path=url_components.path, params=urllib.parse.parse_qs(url_components.query),version_id=version)
            header = MatrixHeader(url=url,
                                    name=url_components.path,
                                    revision_id=revision_id,
                                    storage_method=self.scheme,
                                    memory_style=memory_style)

            self.register.append(url)
            return Matrix(header, content)
        else:
            raise DataBroker.ProtocolException()

    def commit(self, matrix, revisionInfo):
        self._assert_checked_out(matrix.matrix_header.url)
        url_components = urllib.parse.urlparse(matrix.matrix_header.url)
        self.storage_method.storeContent(path=url_components.path,params=urllib.parse.parse_qs(url_components.query),content=matrix.content,revision_info=revisionInfo)
        self.register.remove(matrix.matrix_header.url)

    def release(self, matrix):
        self.register.remove(matrix.matrix_header.url)


