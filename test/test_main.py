import os
import unittest
from nose.tools import raises


testpath = os.path.dirname(__file__)


class Test(unittest.TestCase):
    """ Test main module """

    def test_main(self):
        """ Run main function """
        scenes = main.main(date='2017-01-01', satellite_name='Landsat-8')
        self.assertEqual(len(scenes.scenes), 564)

    @raises(ValueError)
    def _test_main_review_error(self):
        """ Run review feature without envvar set """
        os.setenv('IMGCAT', None)
        scenes = main.main(date='2017-01-01', satellite_name='Landsat-8', review=True)
