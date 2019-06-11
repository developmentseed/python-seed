from .file_storage_method import FileStorageMethod
from isharp.core import AbstractDataBroker
import logging

class SimpleFileBroker(AbstractDataBroker):
    def __init__(self,root_directory):
        super().__init__(FileStorageMethod(root_directory))





