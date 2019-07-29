from unittest import TestCase



class TestNeo(TestCase):


    def setUp(self):
        from neomodel import db
        db.set_connection('bolt://neo4j:neo4j@localhost:7688')



    def test_connect(self):

        self.assertTrue(True)
        pass


