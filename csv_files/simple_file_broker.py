from .file_storage_method import FileStorageMethod
from ishrp_core.broker_impl.abstract_data_broker import AbstractDataBroker


class SimpleFileBroker(AbstractDataBroker):
    def __init__(self,root_directory):
        super().__init__(FileStorageMethod(root_directory),"file")

    def revisions(self, url):
        raise RuntimeError("not supported")





