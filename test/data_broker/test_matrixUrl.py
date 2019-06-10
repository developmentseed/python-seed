from unittest import TestCase

from isharp.core import MatrixUrl


class TestMatrixUrl(TestCase):
    def test_params(self):
        self.assertEqual(
            MatrixUrl("svn://myhost.co.uk:8080/root/index.csv").params(),
            {},
            "test a url without parameters")

        self.assertEqual(
            MatrixUrl("svn://myhost.co.uk:8080/root/inex.csv?param1=value1").params(),
            {"param1": "value1"},
            "testing a url with parameters")

        self.assertEqual(
            MatrixUrl("svn:///root/inex.csv?param1=value1").params(),
            {"param1": "value1"},
            "testing a url with parameters wihout")

        self.assertEqual(
            MatrixUrl("svn://?param1=value1").params(),
            {"param1": "value1"},
            "testing a url with parameters without host or path")

        self.assertEqual(
            MatrixUrl("svn://?param1=").params(),
            {},
            "testing a url with blank param")

        self.assertEqual(
            MatrixUrl("svn://?param1=value1&param2=value2").params(),
            {"param1": "value1","param2": "value2"},
            "testing a url with multi params")


    def test_host(self):
        self.assertEqual(
            MatrixUrl("svn://myhost/path/path2/path3?param1=value1&param2=value2").host(),
            "myhost",
            "testing host name")

        self.assertEqual(
            MatrixUrl("svn://myhost:8080/path/path2/path3").host(),
            "myhost",
            "testing host name with a port number")

        self.assertEqual(
            MatrixUrl("svn:///path/path2/path3").host(),
            None,
            "testing host name with blank host")


    def test_path(self):
        self.assertEqual(
            MatrixUrl("svn://myhost/path/path2/path3?param1=value1&param2=value2").path(),
            "/path/path2/path3",
            "testing path")

        self.assertEqual(
            MatrixUrl("htpp://localhost:8080").path(),
            "",
            "testing  empty path")

    def test_port(self):
        self.assertEqual(
            MatrixUrl("svn://myhost/path/path2/path3?param1=value1&param2=value2").port(),
            None,
            "testing empty port number")

        self.assertEqual(
            MatrixUrl("svn://myhost:8080/path/path2/path3?param1=value1&param2=value2").port(),
            8080,
            "testing non-empty port number")

    def test_scheme(self):
        self.assertEqual(
            MatrixUrl("svn://myhost/path/path2/path3?param1=value1&param2=value2").scheme(),
            "svn",
            "testing scheme")

        self.assertEqual(
            MatrixUrl("myhost:8080/path/path2/path3?param1=value1&param2=value2").port(),
            None,
            "testing empty scheme")
