import os
import tempfile
import shutil
import unittest
import pandas as pd
import datetime
import numpy as np
import test.testutil.pandas_utils as pu
from csv_files.simple_file_broker import SimpleFileBroker
import core.matrix as matrix
from core.data_broker import DataBroker
testpath = os.path.dirname(__file__)


class TestFileDataBroker(unittest.TestCase):

    def setUp(self):
        rows = ['a','b','c','d','e','f','g','h','i','j','k']
        self.test_data_path = tempfile.mkdtemp(prefix="ipp_test_file_data_broker")
        for i in range(1,5):
            df = pu.create_simple_series(rows[:i+2],i+10)
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

    def test_check_in(self):
        m = self.broker.checkout("file://broker.nomura.com/test_sub_1/file_name_1.csv?format=CSV")
        df = m.content
        col_width = len(df.columns)
        original_rows = len(df.index)
        df = df.append(pd.DataFrame(data=np.random.randn(1,col_width),index=[df.index[-1] + datetime.timedelta(days=1)],columns=df.columns))
        m.content = df
        self.broker.commit(m,matrix.RevisionInfo(what="added a row", who="user",when=datetime.datetime.now()))
        m = self.broker.checkout("file://broker.nomura.com/test_sub_1/file_name_1.csv?format=CSV")
        self.assertEquals(len(m.content.index), original_rows +1)


    def test_checkout_file_already_checked_out(self):
        self.broker.checkout("file://broker.nomura.com/test_sub_1/file_name_1.csv?format=CSV")
        with self.assertRaises(DataBroker.CheckoutException):
            self.broker.checkout("file://broker.nomura.com/test_sub_1/file_name_1.csv?format=CSV")

    def test_get_simple_matrix(self):
        m = self.broker.checkout("file://broker.nomura.com/test_sub_1/file_name_1.csv?format=CSV")
        self.assertEqual("/test_sub_1/file_name_1.csv",m.matrix_header.name)
        self.assertEqual("",m.matrix_header.revision_id)
        self.assertEqual('file', m.matrix_header.storage_method)
        self.assertEqual(m.matrix_header.url, "file://broker.nomura.com/test_sub_1/file_name_1.csv?format=CSV")
        self.assertTrue(isinstance(m.content,pd.DataFrame))
        self.assertEqual(m.matrix_header.MemStyles.DATA_FRAME, m.matrix_header.memory_style)
