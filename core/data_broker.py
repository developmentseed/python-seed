import abc


class DataBroker(abc.ABC):

    class CheckoutException(Exception):
        pass

    class ProtocolException(Exception):
        pass

    @abc.abstractmethod
    def checkout(self, url, version_id=None):
        pass

    @abc.abstractmethod
    def commit(self,matrix,revisionInfo):
        pass

    def release(self,matrix):
        pass

    @abc.abstractmethod
    def list(self):
        pass




