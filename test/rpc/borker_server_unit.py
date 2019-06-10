""" Service unit testing best practice.
"""
from nameko.testing.services import worker_factory
from isharp.broker_service.server import DataBrokerService
import pandas as pd
from isharp.core import Matrix
from unittest import TestCase

class TestBrokerService(TestCase):

    def test_broker_service(self):
        broker_service = worker_factory(DataBrokerService)
        broker_service.data_broker_rpc.checkout.side_effect = lambda x: Matrix(None,None,None)
        result = broker_service.data_broker_rpc.checkout("randomRubbish")
        self.assertIsNone(result.matrix_header)