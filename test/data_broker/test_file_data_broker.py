import os
import tempfile
import shutil
import unittest
import pandas as pd
import test.testutil.pandas_utils as pu
from ipp_core.broker_impl.simple_file_broker import SimpleFileBroker
import ipp_core.matrix as matrix
from ipp_core.data_broker import DataBroker
import test.testutil
import xarray


testpath = os.path.dirname(__file__)


class TestFileDataBroker(unittest.TestCase):


    def setUp(self):
        rows = ['a','b','c','d','e','f']
        self.test_data_path = tempfile.mkdtemp(prefix="ipp_test_file_data_broker")
        for i in range(1,5):
            df = pu.create_simple_series(rows[:i],i+10)
            sub_dir = os.path.join(self.test_data_path,"test_sub_{}".format(i))
            os.mkdir(sub_dir)
            fileName = os.path.join(sub_dir,"file_name_{}.csv".format(i))
            df.to_csv(fileName)

        self.broker = SimpleFileBroker(self.test_data_path)

    def tearDown(self):
        shutil.rmtree(self.test_data_path)

    def test_invalid_protocol(self):
        with self.assertRaises(DataBroker.ProtocolException):
            self.broker.checkout("xyz://hello?myParam=1")

    def test_invalid_path(self):
        with self.assertRaises(matrix.StorageMethod.ResourceException):
            self.broker.checkout("file://broker.nomura.com/no_dir/no_file?format=CSV")

    def test_get_simple_matrix(self):
        m = self.broker.checkout("file://broker.nomura.com/test_sub_1/file_name_1.csv?format=CSV")
        self.assertEqual("/test_sub_1/file_name_1.csv",m.matrix_header.name)
        self.assertListEqual([],m.matrix_header.revisions)
        self.assertEqual('file', m.matrix_header.storage_method)
        self.assertEqual(m.matrix_header.url, "file://broker.nomura.com/test_sub_1/file_name_1.csv?format=CSV")
        self.assertTrue(isinstance(m.content,pd.DataFrame))
        self.assertEqual(m.matrix_header.MemStyles.DATA_FRAME, m.matrix_header.memory_style)


