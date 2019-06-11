import unittest
import test.testutil.mongo_arctic_utils as marc
import test.testutil.log_utils as lu
import test.testutil.pandas_utils as pu
from arctic import Arctic
import pandas as pd
import numpy as np
import datetime
from isharp.arctic_broker.broker_impl.arctic_storage_method import  ArcticStorageMethod
from isharp.core import StorageMethod

class TestMongoBroker(unittest.TestCase):
    def setUp(self):
        self.arctic = Arctic('localhost')
        self.library_name = marc.random_library(self.arctic)
        self.symbol_name = 'symbol'
        lu.logger.info("Created test library {}".format(self.library_name))
        self.arctic.initialize_library(self.library_name)
        pd = pu.create_simple_series(['a','b','c'] , 50)
        self.arctic[self.library_name].write(self.symbol_name,pd)

    def tearDown(self):
        self.arctic.delete_library(self.library_name)
        lu.logger.info("deleted test library {}".format(self.library_name))

    def test_acquire_data(self):
        method = ArcticStorageMethod(self.arctic)
        result  = method.acquireContent("{}/symbol".format(self.library_name),{})
        data_frame = result.content
        self.assertIs(3,len(data_frame.columns))
        self.assertIsNone(result.header.description)

    def test_acquire_missing_data(self):
        method = ArcticStorageMethod(self.arctic)
        with self.assertRaisesRegexp(StorageMethod.ResourceException,'^ticker nosymbol not found$'):
            method.acquireContent("{}/nosymbol".format(self.library_name),{})
        with self.assertRaisesRegexp(StorageMethod.ResourceException,'^library nolib not found$'):
            method.acquireContent("nolib/nosymbol".format(self.library_name),{})










