from core.matrix import StorageMethod, MatrixHeader
import pandas as pd
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

    def acquireIndex(self, path):
        csv_file_path = os.path.join(self.base_directory,path.strip("/"))
        index_path = os.path.join(os.path.dirname(csv_file_path),"index.txt")
        return  pd.DataFrame.from_csv(path=index_path)
    def acquireContent(self, path, params,version_id=None):
        super().acquireContent(path,params)
        file_path = os.path.join(self.base_directory, path.strip("/"))
        if (os.path.exists(file_path)):
            content = pd.DataFrame.from_csv(path=file_path)
            return (content, MatrixHeader.MemStyles.DATA_FRAME, "")
        else:
            raise StorageMethod.ResourceException()


    def list(self):
        ret_val = []
        for dir_name,sub_dir_list,file_names in os.walk(self.base_directory):
            index_df =  pd.DataFrame.from_csv(path=os.path.join(dir_name,"index.txt"))

            for index,this_record in index_df.iterrows():
                header = MatrixHeader(this_record['name'],None,self.name,this_record['path'],MatrixHeader.MemStyles.DATA_FRAME)
                ret_val.append(header)
        return ret_val
        # def __init__(self, name, revision_id, storage_method, url, memory_style):