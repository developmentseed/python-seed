from unittest import TestCase
import unittest
import tempfile
import test.testutil.pandas_utils as pu
from csv_files.file_storage_method import  FileStorageMethod
import core.matrix as mtx
import os, shutil
class TestFileStorageMethod(TestCase):
    def setUp(self):
        self.test_data_path = tempfile.mkdtemp(prefix="ipp_test_")
        print("created temp dir {}".format(self.test_data_path))
        self.store=FileStorageMethod(self.test_data_path)
        if not os.path.isdir(self.test_data_path):
            raise Exception("test path {} does not exist".format(self.test_data_path))
    def tearDown(self):
        shutil.rmtree(self.test_data_path)

    def test_invalid_parameters(self):
        file_store_method = FileStorageMethod(self.test_data_path)
        with self.assertRaises(mtx.StorageMethod.ParameterException):
            file_store_method.acquireContent("sample.csv",{"f", "CSV"})

    def test_file_not_found(self):
        file_store_method = FileStorageMethod(self.test_data_path)
        with self.assertRaises(mtx.StorageMethod.ResourceException):
            file_store_method.acquireContent("sample.sss",{"format","CSV"})

    def test_acquireContent(self):
        df = pu.create_simple_series(['a','b','c'],10)
        path = os.path.join(self.test_data_path,"simple.csv")
        df.to_csv(path)
        content = self.store.acquireContent("simple.csv",{"format","CSV"})
        self.assertIsNotNone(content)

if __name__ == '__main__':
    unittest.main()