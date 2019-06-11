from isharp.core import StorageMethod, MatrixHeader, Matrix,MemStyles,AcquireContentReturnValue
import pandas as pd
import os
import logging

logger = logging.getLogger(__name__)

class FileStorageMethod(StorageMethod):
    allowed_formats = ["CSV"]
    def __init__(self, base_directory):
        self.base_directory = base_directory
        if os.path.isdir(self.base_directory):
            logging.info("Found base directory {}".format(self.base_directory))
            super().__init__("file", ["format"])
        else:
            logger.error("could not read base directory {}".format(self.base_directory))
            raise StorageMethod.ResourceException()

    def storeContent(self, path, params, content,revision_info):
        super().storeContent(path, params, content,revision_info)
        file_path = os.path.join(self.base_directory, path.strip("/"))
        if (os.path.exists(file_path)):
            content.to_csv(file_path)
        else:
            raise StorageMethod.ResourceException("invalid file save destination {}".format(path))

    def make_header(self, path):
        csv_file_path = os.path.join(self.base_directory,path.strip("/"))
        index_path = os.path.join(os.path.dirname(csv_file_path),"index.txt")
        index_df = pd.read_csv(index_path, index_col=0)
        index_row = index_df.loc[path, :]
        return MatrixHeader(
                              name=index_row["name"],
                              revision_id=None,
                              storage_method=self.name,
                              memory_style=MemStyles.DATA_FRAME,
                              path = path,
                              description=index_row['description'])

    def acquireContent(self, path, params,version_id=None):
        super().acquireContent(path,params)
        file_path = os.path.join(self.base_directory, path.strip("/"))
        logger.debug("Attempting to acquire file at [{}]  Base dir = [{}] original Path = [{}]".format(file_path,self.base_directory,path))
        if (os.path.exists(file_path)):
            content = pd.read_csv(file_path)
            header = self.make_header(path)
            logger.info("Acquired file for {}".format(path))
            return AcquireContentReturnValue(content=content,header=header)
        else:
            logger.error("could not acquire file for {}".format(path))
            raise StorageMethod.ResourceException()


    def list(self):
        ret_val = []
        for dir_name,sub_dir_list,file_names in os.walk(self.base_directory):
            index_df =  pd.read_csv(os.path.join(dir_name,"index.txt"))
            for index,this_record in index_df.iterrows():
                header = MatrixHeader(
                name=this_record['name'],
                revision_id= None,
                storage_method= self.name,
                path= index,
                memory_style=MemStyles.DATA_FRAME,
                description= this_record["description"]

                )
                ret_val.append(header)
        return ret_val
        # def __init__(self, name, revision_id, storage_method, url, memory_style):