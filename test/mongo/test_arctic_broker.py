import unittest
import test.testutil.mongo_arctic_utils as marc
import test.testutil.log_utils as lu
import test.testutil.pandas_utils as pu
from isharp.datahub.arctic_broker.broker_impl.arctic_data_broker import ArcticBroker
from arctic import Arctic
import pandas as pd
import numpy as np
import datetime
from isharp.datahub.core import RevisionInfo


class TestArcticBroker(unittest.TestCase):

    def setUp(self):
        self.arctic = Arctic('localhost')
        self.library_name = marc.random_library(self.arctic)
        lu.logger.info("Created test library {}".format(self.library_name))
        self.arctic.initialize_library(self.library_name)
        simple_pd =pu.create_simple_series(['a','b','c'],5)
        lib = self.arctic[self.library_name]
        lib.write("symbol",simple_pd)
        lib.write("ES.SETL.EOD", simple_pd)


    def test_checkout_and_checkin_arctic(self):
        url = "arctic:///{}/symbol".format(self.library_name)
        broker = ArcticBroker(self.arctic)
        matrix = broker.checkout(url)
        num_rows_original_version_1 = len(matrix.content.index)
        self.assertEquals("1", matrix.matrix_header.revision_id)
        df  = matrix.content.append(pd.DataFrame(data=np.random.randn(1, len(matrix.content.columns)), index=[matrix.content.index[-1] + datetime.timedelta(days=1)],columns=matrix.content.columns))

        revision_info = RevisionInfo(who="Jeremy Ward", what="first test commit", when=datetime.datetime(year=2000,month=1,day=13))
        broker.commit(matrix.replace_content(df),revision_info)
        matrix = broker.checkout(url)
        self.assertEquals("2", matrix.matrix_header.revision_id)
        num_rows_original_version_2 = len(matrix.content.index)
        self.assertEquals(1, num_rows_original_version_2 - num_rows_original_version_1)
        broker.release(matrix)
        matrix = broker.checkout(url, version="1")
        self.assertEquals(num_rows_original_version_1,len(matrix.content.index))
        broker.release(matrix)

        matrix = broker.checkout(url, version="2")
        self.assertEquals(num_rows_original_version_2,len(matrix.content.index))


    def test_list(self):
        broker = ArcticBroker(self.arctic)
        result = broker.list()
        self.assertEquals(2, len(result))


    def test_peek_with_existing_file(self):
        broker = ArcticBroker(self.arctic)

        url = "arctic:///{}/symbol".format(self.library_name)
        preview = broker.peek(url)

        todays_date = datetime.datetime.now().date()

        expected_start_date =  todays_date- datetime.timedelta(5)
        expected_end_date = expected_start_date + datetime.timedelta(4)

        self.assertEqual(expected_start_date.strftime("%Y-%m-%d"), preview.range_start.strftime("%Y-%m-%d"))
        self.assertEqual(expected_end_date.strftime("%Y-%m-%d"), preview.range_end.strftime("%Y-%m-%d"))

    def test_peek_non_existing_file(self):
        broker = ArcticBroker(self.arctic)
        testurl = "arctic:///subdir_1/file_name_xxx.csv?format=CSV"
        preview = broker.peek(testurl)
        self.assertIsNone(preview)

    def test_with_qualified_ticker_name(self):
        url = "arctic:///{}/ES/SETL/EOD".format(self.library_name)
        broker = ArcticBroker(self.arctic)
        matrix = broker.checkout(url)
        self.assertEqual(matrix.matrix_header.path,"/{}/ES/SETL/EOD".format(self.library_name))





    def tearDown(self):
        self.arctic.delete_library(self.library_name)
        lu.logger.info("deleted test library {}".format(self.library_name))





