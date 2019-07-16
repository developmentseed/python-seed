import unittest
import isharp.yaml_support  as iYaml
import os

class TestYamlConstructors(unittest.TestCase):

    def test_combi_broker(self):
        dn = os.path.dirname(os.path.realpath(__file__))
        yaml_file_path = os.path.join(dn,'combi.yaml')
        context =iYaml.YamlBrokerContext(yaml_file_path)





