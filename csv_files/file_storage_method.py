from core.matrix import StorageMethod, MatrixHeader
import pandas as pd
import xarray
import os


class FileStorageMethod(StorageMethod):
    allowed_formats = ["CSV"]
    def __init__(self, base_directory):
        self.base_directory = base_directory
        super().__init__("file", ["format"])

    def storeContent(self, path, params, content,revision_info):
        super().storeContent(path, params, content,revision_info)
        file_path = os.path.join(self.base_directory, path.strip("/"))
        if (os.path.exists(file_path)):
            content.to_csv(file_path)
        else:
            raise StorageMethod.ResourceException("invalid file save destination {}".format(path))


    def acquireContent(self, path, params):
        super().acquireContent(path,params)
        file_path = os.path.join(self.base_directory, path.strip("/"))
        if (os.path.exists(file_path)):
            content = pd.DataFrame.from_csv(path=file_path)
            return (content, MatrixHeader.MemStyles.DATA_FRAME, [])
        else:
            raise StorageMethod.ResourceException()

