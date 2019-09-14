import os
import shutil
import tempfile
import unittest
import pandas as pd
import datetime
import test.testutil.file_utils as fu

import test.testutil.log_utils as lu
from isharp.datahub.core import StorageMethod, MemStyles
from isharp.datahub.csv_files.simple_file_broker import SimpleFileBroker

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



    def test_invalid_path(self):
        with self.assertRaises(StorageMethod.ResourceException):
            self.broker.checkout("file://broker.nomura.com/no_dir/no_file?format=CSV")

    def test_get_compound_path(self):
        testurl = "file:///subdir_1/file_name_1.csv?format=CSV"
        m = self.broker.checkout(testurl)
        self.assertEqual("file_name_1.csv",m.matrix_header.name)
        self.assertEqual("subdir_1/file_name_1.csv", m.matrix_header.path)



    def test_peek_with_existing_file(self):
        testurl = "file:///subdir_1/file_name_1.csv?format=CSV"
        preview = self.broker.peek(testurl)

        todays_date = datetime.datetime.now().date()

        expected_start_date =  todays_date- datetime.timedelta(11)
        expected_end_date = expected_start_date + datetime.timedelta(10)

        self.assertEqual(expected_start_date.strftime("%Y-%m-%d"), preview.range_start)
        self.assertEqual(expected_end_date.strftime("%Y-%m-%d"), preview.range_end)


    def test_peek_non_existing_file(self):
        testurl = "file:///subdir_1/file_name_xxx.csv?format=CSV"
        preview = self.broker.peek(testurl)
        self.assertIsNone(preview)


    def test_get_simple_matrix(self):
        testurl = "file:///file_name_1.csv?format=CSV"
        m = self.broker.checkout(testurl)
        self.assertEqual("file_name_1.csv",m.matrix_header.name)
        self.assertEqual(None,m.matrix_header.revision_id)
        self.assertEqual('file', m.matrix_header.storage_method)
        self.assertEqual(m.matrix_header.path, "file_name_1.csv")
        self.assertTrue(isinstance(m.content,pd.DataFrame))
        self.assertEqual(MemStyles.DATA_FRAME, m.matrix_header.memory_style)

    def test_list(self):
        headers = self.broker.list()
        self.assertEquals(14,len(headers))
        header  = headers[0]
        self.assertIsNone(header.revision_id)
        self.assertEqual("file",header.storage_method)
        self.assertEqual("file_name_1.csv", header.path)
        self.assertEqual("file_name_1.csv",header.name)
        self.assertEqual("description of file_name_1.csv",header.description)
        self.assertEqual(MemStyles.DATA_FRAME, header.memory_style)

