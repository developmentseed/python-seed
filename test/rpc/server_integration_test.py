""" Service integration testing best practice.
"""

from unittest import TestCase


class TestServerIntegration(TestCase):
    def setUp(self):
        pass

    def test_one(self):
        self.assertEqual(1,1)