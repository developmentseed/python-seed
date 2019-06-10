
import unittest
from isharp.core import DataBroker,MatrixHeader,Matrix,AcquireContentReturnValue,Revision
from unittest.mock import MagicMock
from unittest.mock import patch
from isharp.core import StorageMethod
from datetime import datetime
from isharp.core import RevisionInfo
from isharp.core import AbstractDataBroker

test_header = MatrixHeader(name="hello", revision_id=5, storage_method="test", path=".", memory_style=None,
                           description="None")
test_content = {}
time_now = datetime.now()

test_revision = Revision("abc",RevisionInfo("who","what",time_now))

class TestAbstractBroker(unittest.TestCase):
    @patch.multiple(StorageMethod, __abstractmethods__=set())
    def setUp(self):
        self.mock_storage_method = StorageMethod("test")
        self.broker = AbstractDataBroker(self.mock_storage_method)

    def tearDown(self):
        pass

    def test_invalid_protocol(self):
        with self.assertRaises(DataBroker.ProtocolException):
            self.broker.checkout("xyz://hello?myParam=1")

    def test_checkout_file_already_checked_out(self):
        self.mock_acquire_content_result()
        self.broker.checkout("test:///file_name_1.csv?format=CSV")
        with self.assertRaises(DataBroker.CheckoutException):
            self.broker.checkout("test:///file_name_1.csv?format=CSV")

    def test_commit(self):
        self.mock_acquire_content_result()
        self.mock_commit_result()
        testurl = "test:///file_name_1.csv?format=CSV"
        m = self.broker.checkout(testurl)
        revision_info = RevisionInfo("who","what",time_now)
        revision = self.broker.commit(m,revision_info)
        self.assertEqual(revision_info,revision.revision_info)

    def test_release(self):
        self.mock_acquire_content_result()
        self.mock_commit_result()
        testurl = "test:///file_name_1.csv?format=CSV"
        m = self.broker.checkout(testurl)
        self.broker.release(m)
        with self.assertRaises(DataBroker.CheckoutException):
            revision = self.broker.commit(m, test_revision.revision_info)


    def test_get_simple_matrix(self):
        self.mock_acquire_content_result()
        testurl = "test:///file_name_1.csv?format=CSV"
        m = self.broker.checkout(testurl)
        self.assertEqual(test_header, m.matrix_header,"header should be test header")
        self.assertEqual(test_content, m.content,"Content should be empty hashtable")
        self.assertEqual(testurl,m.url.url, "URL should be test url")
        self.mock_storage_method.acquireContent.assert_called_once_with(params={"format": "CSV"}, path="/file_name_1.csv",version_id =None)

    def test_list(self):
        self.mock_storage_method.list = MagicMock(return_value=[test_header])
        self.assertEqual([test_header],self.broker.list(),"Sould return single header")
        self.mock_storage_method.list.assert_called_once()

    def mock_commit_result(self):
        self.mock_storage_method.storeContent = MagicMock(return_value=test_revision)

    def mock_acquire_content_result(self):
        self.mock_storage_method.acquireContent = \
            MagicMock(return_value=(AcquireContentReturnValue(header=test_header,content=test_content)))
