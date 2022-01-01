import os
import shutil
import tempfile
import unittest
import pandas as pd
import datetime
import random
import test.testutil.file_utils as fu
from github import Github, InputGitAuthor
import test.testutil.log_utils as lu
import test.testutil.pandas_utils as pu
import test.testutil.github_utils as gu
from isharp.datahub.core import StorageMethod, MemStyles
from isharp.datahub.github_broker.broker_impl.github_data_broker import GithubBroker
from isharp.datahub.github_broker.broker_impl.github_storage_method import GithubStorageMethod
rows = ['a','b','c','d','e','f','g','h','i','j','k']

author = InputGitAuthor(
        "jeremycward",
        "jeremy_c_ward@yahoo.co.uk"
)

class TestGithubDataBroker(unittest.TestCase):

    def setUp(self):
        self.branch = 'main'
        self.repo_name = "jeremycward/datahubtest"
        self.gitfile = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz___') for i in range(16))
        self.token = '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'
        self.initialTag = ''.join(random.choice('1234567890') for i in range(10))
        df = pu.create_simple_series(rows,  10)
        self.repo = gu.GitTestRepo(self.token,self.repo_name)
        self.repo.create_and_tag(author,self.gitfile,df,self.initialTag,self.branch)

        self.broker = GithubBroker(self.token,self.repo_name)


    def tearDown(self):
        pass



    # def test_invalid_path(self):
    #     with self.assertRaises(StorageMethod.ResourceException):
    #         self.broker.checkout("file://broker.nomura.com/no_dir/no_file?format=CSV")
    #
    # def test_get_compound_path(self):
    #     testurl = "file:///subdir_1/file_name_1.csv?format=CSV"
    #     m = self.broker.checkout(testurl)
    #     self.assertEqual("file_name_1.csv",m.matrix_header.name)
    #     self.assertEqual("subdir_1/file_name_1.csv", m.matrix_header.path)
    #
    #
    #
    def test_peek_with_existing_file(self):
        testurl = "github:///{}?branch=main".format(self.gitfile)
        preview = self.broker.peek(testurl)
        print(preview.range_start)
        print(preview.range_end)
        self.assertEqual(0, preview.range_start)
        self.assertEqual(9, preview.range_end)
        self.assertEqual(self.initialTag,preview.header.revision_id)

        #
        # todays_date = datetime.datetime.now().date()
        #
        # expected_start_date =  todays_date- datetime.timedelta(11)
        # expected_end_date = expected_start_date + datetime.timedelta(10)
        #
    #
    #
    # def test_peek_non_existing_file(self):
    #     testurl = "file:///subdir_1/file_name_xxx.csv?format=CSV"
    #     preview = self.broker.peek(testurl)
    #     self.assertIsNone(preview)
    #
    #
    # def test_get_simple_matrix(self):
    #     testurl = "file:///file_name_1.csv?format=CSV"
    #     m = self.broker.checkout(testurl)
    #     self.assertEqual("file_name_1.csv",m.matrix_header.name)
    #     self.assertEqual(None,m.matrix_header.revision_id)
    #     self.assertEqual('file', m.matrix_header.storage_method)
    #     self.assertEqual(m.matrix_header.path, "file_name_1.csv")
    #     self.assertTrue(isinstance(m.content,pd.DataFrame))
    #     self.assertEqual(MemStyles.DATA_FRAME, m.matrix_header.memory_style)
    #
    # def test_list(self):
    #     headers = self.broker.list()
    #     self.assertEquals(14,len(headers))
    #     header  = headers[0]
    #     self.assertIsNone(header.revision_id)
    #     self.assertEqual("file",header.storage_method)
    #     self.assertEqual("file_name_1.csv", header.path)
    #     self.assertEqual("file_name_1.csv",header.name)
    #     self.assertEqual("description of file_name_1.csv",header.description)
    #     self.assertEqual(MemStyles.DATA_FRAME, header.memory_style)

