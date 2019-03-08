import abc


class DataBroker(abc.ABC):
    @abc.abstractmethod
    def checkout(self, url):
        pass

    @abc.abstractmethod
    def checkout(self,url,revisionId):
        pass

    @abc.abstractmethod
    def commit(self,matrix):
        pass

    @abc.abstractmethod
    def revisions(self,url):
        pass

    @abc.abstractmethod
    def catalogue(self):
        pass




