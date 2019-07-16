from unittest import TestCase
import os
import isharp.broker_service.server as main_app
config_path = "../../docker_images/datahub/config.yaml"
class TestServerIntegration(TestCase):

    def setup(self):
        print(config_path)

    def test_initialisation(self):
        config_dir = os.path.dirname(__file__)
        config_path = os.path.join(config_dir,"datahub_config.yaml")
        main_app.start_datahub(config_path)

