import unittest
import test.testutil.mongo_arctic_utils as marc
import test.testutil.log_utils as lu
import test.testutil.pandas_utils as pu
import random
import string
from arctic import Arctic
import pandas as pd
import numpy as np
import datetime
from isharp.datahub.arctic_broker.broker_impl.arctic_storage_method import  ArcticStorageMethod, add_revision_to_metadata,get_revisions_from_metadata,import_pandas
from isharp.datahub.core import StorageMethod, MatrixUrl,Revision,RevisionInfo
from test.testutil import randomString




class TestMongoBroker(unittest.TestCase):
    def setUp(self):
        self.username = randomString()
        self.time_now = datetime.datetime.now()
        self.arctic = Arctic('localhost')
        self.library_name = marc.random_library(self.arctic)
        self.symbol_name = 'symbol'
        self.qualified_symbol_name = "ES.SETL.EOD"
        self.qualified_symbol_name_as_path = self.qualified_symbol_name.replace('.','/')
        lu.logger.info("Created test library {}".format(self.library_name))
        self.arctic.initialize_library(self.library_name)
        pd = pu.create_simple_series(['a','b','c'] , 50)
        import_pandas(self.arctic[self.library_name],pd,self.symbol_name,RevisionInfo(who=self.username, what="init", when=self.time_now))
        import_pandas(self.arctic[self.library_name],pu.create_simple_series(['a','b','c','d'] , 75),self.qualified_symbol_name,
                      RevisionInfo(who=self.username, what="init qualified", when=self.time_now))

    def tearDown(self):
        self.arctic.delete_library(self.library_name)
        lu.logger.info("deleted test library {}".format(self.library_name))

    def test_acquire_data(self):
        method = ArcticStorageMethod(self.arctic)
        result  = method.acquireContent("{}/symbol".format(self.library_name),{})
        data_frame = result.content
        self.assertFalse(result.header.path[0] == '/')
        self.assertIs(3,len(data_frame.columns))
        self.assertIsNone(result.header.description)
        self.assertEqual(result.header.name,result.header.path)


    def test_history(self):
        method = ArcticStorageMethod(self.arctic)
        url = MatrixUrl("{}/symbol".format(self.library_name))
        result = method.history(url)
        self.assertEquals(1,len(result))


    def test_acquire_data_with_qualified_symbol(self):
        method = ArcticStorageMethod(self.arctic)
        url = "{}/{}".format(self.library_name,self.qualified_symbol_name_as_path)
        result  = method.acquireContent(url,{})
        data_frame = result.content
        self.assertIs(4,len(data_frame.columns))


    def test_revision_storage(self):
        time_now = datetime.datetime.now()
        info = RevisionInfo(who="aPerson",what="a Change", when=time_now)

        metadata = {}
        add_revision_to_metadata(Revision("1",info),metadata)
        info2 = RevisionInfo(who="anotherPerson", what="anotherChange", when=time_now)
        add_revision_to_metadata( Revision("2", info2), metadata)

        revs = get_revisions_from_metadata(metadata)
        self.assertEquals(2,len(revs))
        revision = revs[0]
        self.assertEquals("1",revision.id)
        self.assertEquals("a Change", revision.revision_info.what)
        self.assertEquals("aPerson", revision.revision_info.who)
        self.assertEquals(time_now, revision.revision_info.when)

        revision = revs[1]
        self.assertEquals("2",revision.id)
        self.assertEquals("anotherChange", revision.revision_info.what)
        self.assertEquals("anotherPerson", revision.revision_info.who)
        self.assertEquals(time_now, revision.revision_info.when)



    def test_acquire_missing_data(self):
        method = ArcticStorageMethod(self.arctic)
        with self.assertRaisesRegexp(StorageMethod.ResourceException,'^ticker nosymbol not found$'):
            method.acquireContent("{}/nosymbol".format(self.library_name),{})
        with self.assertRaisesRegexp(StorageMethod.ResourceException,'^library nolib not found in library list'):
            method.acquireContent("nolib/nosymbol".format(self.library_name),{})









