
from isharp.broker_client.remote_proxy import BrokerConnectionPool
import logging
logging.basicConfig()
logger = logging.getLogger()


# create console handler and set level to info
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

logger = logging.getLogger(__name__)


logger.info("hello from logging")


with BrokerConnectionPool() as broker:
    # print(broker.checkout("file://ec2-34-205-159-121.compute-1.amazonaws.com:5672/file_name_1.csv?format=CSV").matrix_header.description)
    # print(broker.checkout("file://ec2-34-205-159-121.compute-1.amazonaws.com:5672/file_name_2.csv?format=CSV").matrix_header.description)
    # print(broker.checkout("file://ec2-34-205-159-121.compute-1.amazonaws.com:5672/subdir_2/subdir_1/file_name_1.csv?format=CSV").matrix_header.description)

    print(broker.list("ec2-34-205-159-121.compute-1.amazonaws.com:5672"))


print("end")


