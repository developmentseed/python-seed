from ipp_core.matrix import StorageMethod
import pandas as pd
import xarray
import os


class FileStorageMethod(StorageMethod):
    allowed_formats = ["CSV"]
    def __init__(self, base_directory):
        self.base_directory = base_directory
        super().__init__("file", ["format"])

    def storeContent(self, path, params, content):
        super().storeContent(path, params, content)
        file_path = os.path.join(self.base_directory, path.strip("/"))
        if (os.path.exists(file_path)):
            content.to_csv(file_path)

        else:
            raise StorageMethod.ResourceException("invalid file save destination {}".format(path))



    def acquireContent(self, path, params):
        for required_param in self.required_parameters:
            if not required_param in params:
                raise self.ParameterException("format parameter missing or unset")
        file_path = os.path.join(self.base_directory, path.strip("/"))
        if (os.path.exists(file_path)):
            return pd.DataFrame.from_csv(path=file_path)

        else:
            raise StorageMethod.ResourceException()

