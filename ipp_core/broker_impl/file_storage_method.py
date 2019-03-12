from ipp_core.matrix import StorageMethod
import pandas as pd
import xarray
import os


class FileStorageMethod(StorageMethod):
    allowed_formats = ["CSV"]
    def __init__(self, base_directory):
        self.base_directory = base_directory
        super().__init__("file", ["format"])

    def acquireContent(self, path, params):
        for required_param in self.required_parameters:
            if not required_param in params:
                raise self.ParameterException("format parameter missing or unset")
        file_path = os.path.join(self.base_directory, path.strip("/"))
        if (os.path.exists(file_path)):
            df = pd.DataFrame.from_csv(path=file_path)
            return xarray.Dataset.from_dataframe(df)
        else:
            raise StorageMethod.ResourceException()

