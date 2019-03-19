import abc


class DataBroker(abc.ABC):
    class SCMRegistry:
        def __init__(self):
            self.register = []

        def checkout(self, url):
            if (url in self.register):
                raise DataBroker.CheckoutException("matrix [{}] is already checked out".format(url))
            else:
                self.register.append(url)

        def checkin(self,url):
            if (url not in self.register):
                raise DataBroker.CheckoutException("matrix [{}] is not already checked out".format(url))
            else:
                self.register.remove(url)

    class CheckoutException(Exception):
        pass

    class ProtocolException(Exception):
        pass

    def __init__(self):
        self.scm_registry = DataBroker.SCMRegistry()
    @abc.abstractmethod
    def checkout(self, url):
        self.scm_registry.checkout(url)

    @abc.abstractmethod
    def commit(self,matrix,revisionInfo):
        self.scm_registry.checkin(matrix.matrix_header.url)

    @abc.abstractmethod
    def catalogue(self):
        pass



