import os
import unittest
from ipp_core.broker_impl.SimpleDataBroker import SimpleBroker

testpath = os.path.dirname(__file__)


class TestDataBroker(unittest.TestCase):
    """ Test main module """

    def test_main(self):
        headers = []
        broker = SimpleBroker(headers)

