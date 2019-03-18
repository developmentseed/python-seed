import unittest
import  test.testutil.mongo_arctic_utils as marc
import  test.testutil.log_utils as lu
import  test.testutil.pandas_utils as pu
from arctic import Arctic
import pandas as pd
import numpy as np
import datetime







class TestMongoBroker(unittest.TestCase):

    def setUp(self):
        self.arctic = Arctic('localhost')
        self.library_name = marc.random_library(self.arctic)
        lu.logger.info("Created test library {}".format(self.library_name))
        self.arctic.initialize_library(self.library_name)
        simple_pd =pu.create_simple_series(['a','b','c'],5)
        lib = self.arctic[self.library_name]
        lib.write("symbol",simple_pd)
        # create a second version
        df = lib.read('symbol').data
        df = simple_pd.append(
            pd.DataFrame(data=np.random.randn(1, len(df.columns)), index=[df.index[-1] + datetime.timedelta(days=1)],
                         columns=df.columns))
        lib.write("symbol",df)
        lu.logger.info("wrote second version {}".format(df))
        lu.logger.info("versions  now {}".format(lib.list_versions('symbol')))


    def tearDown(self):
        self.arctic.delete_library(self.library_name)
        lu.logger.info("deleted test library {}".format(self.library_name))


    def test_checkout_and_checkin_arctic(self):
        libs = self.arctic.list_libraries()
        self.assertIn(self.library_name,libs)







