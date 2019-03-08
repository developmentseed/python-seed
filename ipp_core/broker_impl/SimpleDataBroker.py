from ..DataBroker import DataBroker
class SimpleBroker(DataBroker):
    def __init__(self,matrix_headers):
        self.matrix_headers = matrix_headers

    def checkout(self, url):
        pass

    def commit(self, matrix,revision_info):
        pass

    def revisions(self, url):
        pass

    def catalogue(self):
        return self.matrix_headers




