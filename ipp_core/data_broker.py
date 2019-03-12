import abc


class DataBroker(abc.ABC):
    class ProtocolException(Exception):
        pass

    @abc.abstractmethod
    def checkout(self, url):
        pass

    @abc.abstractmethod
    def commit(self,matrix,revisionInfo):
        pass

    @abc.abstractmethod
    def catalogue(self):
        pass




