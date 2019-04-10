import os
import tempfile
import shutil
import unittest
import pandas as pd
import datetime
import numpy as np
import test.testutil.log_utils as lu
import test.testutil.pandas_utils as pu
import test.testutil.file_utils as fu
from csv_files.simple_file_broker import SimpleFileBroker
import core.matrix as matrix
from core.data_broker import DataBroker
testpath = os.path.dirname(__file__)


class TestFileDataBroker(unittest.TestCase):

    def setUp(self):
        rows = ['a','b','c','d','e','f','g','h','i','j','k']
        self.test_data_path = tempfile.mkdtemp(prefix="ipp_test_file_data_broker")
        lu.logger.info("test file path: {}" + self.test_data_path)

        fu.make_file_tree(self.test_data_path,2,3)
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
        testurl="file:///file_name_1.csv?format=CSV"
        m = self.broker.checkout(testurl)
        df = m.content
        col_width = len(df.columns)
        original_rows = len(df.index)
        df = df.append(pd.DataFrame(data=np.random.randn(1,col_width),index=[df.index[-1] + datetime.timedelta(days=1)],columns=df.columns))
        m.content = df
        self.broker.commit(m,matrix.RevisionInfo(what="added a row", who="user",when=datetime.datetime.now()))
        m = self.broker.checkout(testurl)
        self.assertEquals(len(m.content.index), original_rows +1)


    def test_checkout_file_already_checked_out(self):
        self.broker.checkout("file:///file_name_1.csv?format=CSV")
        with self.assertRaises(DataBroker.CheckoutException):
            self.broker.checkout("file:///file_name_1.csv?format=CSV")

    def test_get_simple_matrix(self):
        m = self.broker.checkout("file:///file_name_1.csv?format=CSV")
        self.assertEqual("file_name_1.csv",m.matrix_header.name)
        self.assertEqual("",m.matrix_header.revision_id)
        self.assertEqual('file', m.matrix_header.storage_method)
        self.assertEqual(m.matrix_header.url, "file:///file_name_1.csv?format=CSV")
        self.assertTrue(isinstance(m.content,pd.DataFrame))
        self.assertEqual(m.matrix_header.MemStyles.DATA_FRAME, m.matrix_header.memory_style)

    def test_list(self):
        headers = self.broker.list()
        self.assertEquals(14,len(headers))
        header  = headers[0]
        self.assertIsNone(header.revision_id)
        self.assertEqual("file",header.storage_method)
        self.assertEqual("file_name_1.csv",header.name)
        self.assertEqual("description of file_name_1.csv",header.description)
        self.assertEqual(matrix.MatrixHeader.MemStyles.DATA_FRAME, header.memory_style)


