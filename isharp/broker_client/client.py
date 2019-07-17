
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
    mtx = broker.checkout("file://ec2-34-205-159-121.compute-1.amazonaws.com:5672/file_name_1.csv?format=CSV")
    broker.release(mtx)
    print (mtx.content)
    mtx = broker.checkout("file://ec2-34-205-159-121.compute-1.amazonaws.com:5672/file_name_1.csv?format=CSV")
    print (mtx.matrix_header.description)
    broker.release(mtx)




print("end")


