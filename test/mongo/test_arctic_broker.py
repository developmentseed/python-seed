import unittest
import test.testutil.mongo_arctic_utils as marc
import test.testutil.log_utils as lu
import test.testutil.pandas_utils as pu
from isharp.datahub.arctic_broker.broker_impl.arctic_data_broker import ArcticBroker
from isharp.datahub.arctic_broker.broker_impl.arctic_storage_method import  add_revision_to_metadata,get_revisions_from_metadata,history_tag,import_pandas
from arctic import Arctic
import pandas as pd
import numpy as np
import datetime
from isharp.datahub.core import RevisionInfo

class TestArcticBroker(unittest.TestCase):

    def setUp(self):
        self.robot_user = "robot"
        self.import_comment = "importcomment"
        self.arctic = Arctic('localhost')
        self.library_name = marc.random_library(self.arctic)
        lu.logger.info("Created test library {}".format(self.library_name))
        self.arctic.initialize_library(self.library_name)
        simple_pd =pu.create_simple_series(['a','b','c'],5)
        lib = self.arctic[self.library_name]

        import_pandas(lib,simple_pd,"symbol",RevisionInfo(who=self.robot_user,what=self.import_comment, when = datetime.datetime.now()))
        import_pandas(lib,simple_pd,"ES.SETL.EOD",RevisionInfo(who=self.robot_user,what="import something else", when = datetime.datetime.now()))

    def tearDown(self):
        self.arctic.delete_library(self.library_name)
        lu.logger.info("deleted test library {}".format(self.library_name))


    def test_checkout_and_checkin_arctic(self):
        url = "arctic:///{}/symbol".format(self.library_name)
        broker = ArcticBroker(self.arctic)
        matrix = broker.checkout(url)
        history = broker.history(url)
        self.assertEqual(1, len(history))
        self.assertEqual(self.robot_user,history[0].revision_info.who)
        self.assertEqual("1", history[0].id)
        self.assertEqual(self.import_comment, history[0].revision_info.what)
        num_rows_original_version_1 = len(matrix.content.index)

        df  = matrix.content.append(pd.DataFrame(data=np.random.randn(1, len(matrix.content.columns)), index=[matrix.content.index[-1] + datetime.timedelta(days=1)],columns=matrix.content.columns))
        revision_info = RevisionInfo(who="Jeremy Ward", what="first test commit", when=datetime.datetime(year=2000,month=1,day=13))
        broker.commit(matrix.replace_content(df),revision_info)
        hist = broker.history(url)
        self.assertEqual(2,len(hist))
        self.assertEqual(hist[1].revision_info.what,"first test commit")
        self.assertEqual("2", hist[1].id)
        matrix = broker.checkout(url)


        num_rows_original_version_2 = len(matrix.content.index)
        self.assertEquals(1, num_rows_original_version_2 - num_rows_original_version_1)
        broker.release(matrix)
        original_version = broker.history(url)[0].id
        matrix = broker.checkout(url, original_version)
        self.assertEqual(num_rows_original_version_1,len(matrix.content.index))
        broker.release(matrix)

        version_2 = broker.history(url)[1].id
        matrix = broker.checkout(url, version=version_2)
        self.assertEquals(num_rows_original_version_2,len(matrix.content.index))
        broker.release(matrix)
        self.assertEqual(2,len(broker.history(url)))


    def test_list(self):
        broker = ArcticBroker(self.arctic)
        result = broker.list()
        self.assertEquals(2, len(result))
        self.assertEqual("{}/ES/SETL/EOD".format(self.library_name),result[0].path)


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





