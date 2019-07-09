import os
import test.testutil.pandas_utils as pu
import pandas as pd
import pathlib
rows = ['a','b','c','d','e','f','g','h','i','j','k']

def fill_directory_with_content(root_directory,directory_path, number_files):
    index_data =[]
    key_data = []
    for i in range(1, number_files):
        df = pu.create_simple_series(rows[:i + 2], i + 10)
        file_name = "file_name_{}.csv".format(i)
        filepath = os.path.join(root_directory,directory_path, file_name)
        df.to_csv(filepath)
        posix_path  = pathlib.PureWindowsPath(os.path.join("/",directory_path,file_name))
        key_data.append(posix_path.as_posix())
        index_data.append((file_name,"description of {}".format(file_name)))

    df = pd.DataFrame( index=pd.Index(key_data,name="path"),data=index_data, columns=["name", "description"])

    index_file_path = os.path.join(root_directory,directory_path, "index.txt")
    df.to_csv(index_file_path)


def make_file_tree(root_directory_path,tree_depth, files_per_directory,relative_path=''):

    for i in range(1, files_per_directory):
        fill_directory_with_content(root_directory_path,relative_path,files_per_directory)
        if tree_depth > 0:
            new_relative_path = os.path.join(relative_path,"subdir_{}".format(i))
            actual_directory_path =os.path.join(root_directory_path,new_relative_path)
            os.mkdir(actual_directory_path)
            make_file_tree(root_directory_path, tree_depth-1, files_per_directory,new_relative_path)






