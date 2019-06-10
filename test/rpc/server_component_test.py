from isharp.core import StorageMethod,AbstractDataBroker,Matrix,MatrixHeader,AcquireContentReturnValue
from nameko.testing.services import worker_factory
from isharp.broker_service.server import DataBrokerService
from unittest import TestCase
from unittest.mock import patch
from unittest.mock import MagicMock

test_header = MatrixHeader(name="hello", revision_id=5, storage_method="test", path=".", memory_style=None,
                           description="None")
test_content = {}

class ServerComponentTest(TestCase):

    @patch.multiple(StorageMethod, __abstractmethods__=set())
    def setUp(self):
        self.mock_storage_method = StorageMethod("test")
        self.broker = AbstractDataBroker(self.mock_storage_method)

    def tearDown(self):
        pass


    def test_service_checkout(self):
        testurl = "test:///file_name_1.csv?format=CSV"
        self.mock_storage_method.acquireContent=MagicMock(return_value=(AcquireContentReturnValue(header=test_header, content=test_content)))
        service = worker_factory(DataBrokerService, delegate=self.broker)
        result = service.checkout(testurl)
        self.assertEqual(5,result.matrix_header.revision_id)
