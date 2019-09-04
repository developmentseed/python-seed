import unittest
import test.testutil.mongo_arctic_utils as marc
import test.testutil.log_utils as lu
import test.testutil.pandas_utils as pu
from arctic import Arctic
import pandas as pd
import numpy as np
import datetime
from isharp.datahub.arctic_broker.broker_impl.arctic_storage_method import  ArcticStorageMethod
from isharp.datahub.core import StorageMethod

class TestMongoBroker(unittest.TestCase):
    def setUp(self):
        self.arctic = Arctic('localhost')
        self.library_name = marc.random_library(self.arctic)
        self.symbol_name = 'symbol'
        self.qualified_symbol_name = "ES.SETL.EOD"
        self.qualified_symbol_name_as_path = self.qualified_symbol_name.replace('.','/')
        lu.logger.info("Created test library {}".format(self.library_name))
        self.arctic.initialize_library(self.library_name)
        pd = pu.create_simple_series(['a','b','c'] , 50)
        self.arctic[self.library_name].write(self.symbol_name,pd)
        self.arctic[self.library_name].write(self.qualified_symbol_name, pu.create_simple_series(['a','b','c','d'] , 75))

    def tearDown(self):
        self.arctic.delete_library(self.library_name)
        lu.logger.info("deleted test library {}".format(self.library_name))

    def test_acquire_data(self):
        method = ArcticStorageMethod(self.arctic)
        result  = method.acquireContent("{}/symbol".format(self.library_name),{})
        data_frame = result.content
        self.assertIs(3,len(data_frame.columns))
        self.assertIsNone(result.header.description)

    def test_acquire_data_with_qualified_symbol(self):
        method = ArcticStorageMethod(self.arctic)
        url = "{}/{}".format(self.library_name,self.qualified_symbol_name_as_path)
        result  = method.acquireContent(url,{})
        data_frame = result.content
        self.assertIs(4,len(data_frame.columns))




    def test_acquire_missing_data(self):
        method = ArcticStorageMethod(self.arctic)
        with self.assertRaisesRegexp(StorageMethod.ResourceException,'^ticker nosymbol not found$'):
            method.acquireContent("{}/nosymbol".format(self.library_name),{})
        with self.assertRaisesRegexp(StorageMethod.ResourceException,'^library nolib not found in library list'):
            method.acquireContent("nolib/nosymbol".format(self.library_name),{})










