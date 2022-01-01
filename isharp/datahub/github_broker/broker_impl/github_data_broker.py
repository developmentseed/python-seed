from isharp.datahub.core import DataBroker,Matrix,AbstractDataBroker
from .github_storage_method import GithubStorageMethod

class GithubBroker(AbstractDataBroker):
    def __init__(self,token,repo_name):
        super().__init__(GithubStorageMethod(token,repo_name))

    def checkout(self, url,version=None):
        return super().checkout(url,version)

    def commit(self, matrix, revisionInfo):
        super().commit(matrix, revisionInfo)






