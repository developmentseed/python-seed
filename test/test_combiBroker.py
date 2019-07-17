from unittest import TestCase
from unittest.mock import MagicMock,patch,Mock
from isharp.core import DataBroker,CombiBroker, MatrixUrl, MatrixHeader,Matrix

class TestCombiBroker(TestCase):

    @patch.multiple(DataBroker, __abstractmethods__=set())
    def setUp(self):
        self.foo_broker = Mock()
        self.bar_broker = Mock()
        self.foo_broker.list = MagicMock(return_value=[
            MatrixHeader(name="foo",revision_id=None,storage_method=None,path=None,memory_style=None,description=None),
            MatrixHeader(name="foo_2", revision_id=None, storage_method=None, path=None, memory_style=None,description=None)
        ])
        self.bar_broker.list = MagicMock(return_value = [MatrixHeader(name="bar",revision_id=None,storage_method=None,path=None,memory_style=None,description=None)])
        self.combi_broker = CombiBroker(
            {
                "foo": self.foo_broker,
                "bar": self.bar_broker
            }
        )

    def test_checkout_with_invalid_protocol(self):
        with self.assertRaises(DataBroker.ProtocolException):
            self.combi_broker.checkout("test:///file_name_1.csv?format=CSV")

    def test_checkout_with_valid_protocol(self):
        self.combi_broker.checkout("foo://abc.com/xyz")
        self.bar_broker.checkout.assert_not_called()
        self.foo_broker.checkout.assert_called_with("foo://abc.com/xyz",None)

    def test_checkin_with_valid_protocol(self):
        m = Matrix(matrix_header=None,content=None, url = MatrixUrl("foo://abc.com/xyz"))
        ri=None
        self.combi_broker.commit(m,ri)
        self.bar_broker.commit.assert_not_called()
        self.foo_broker.commit.assert_called_with(m,ri)
        self.foo_broker.checkout.assert_not_called()
        self.bar_broker.checkout.assert_not_called()
        self.foo_broker.checkout.assert_not_called()

    def test_checkin_with_invalid_protocol(self):
        with self.assertRaises(DataBroker.ProtocolException):
            m = Matrix(matrix_header=None, content=None, url=MatrixUrl("test://abc.com/xyz"))
            ri = None
            self.combi_broker.commit(m, ri)

    def test_list(self):
        ret = self.combi_broker.list()
        self.assertEquals(3, len(ret))
        self.foo_broker.list.assert_called()
        self.bar_broker.list.assert_called()
        self.bar_broker.checkout.assert_not_called()
        self.foo_broker.checkout.assert_not_called()










