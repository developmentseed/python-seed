
from isharp.broker_client.remote_proxy import BrokerConnectionPool
from  isharp.broker_client.client_utils import mtx_headers_as_dataframe as to_df
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
    mtx = broker.checkout("file://localhost:5672/file_name_1.csv?format=CSV")
    print(mtx.content)
    broker.release(mtx)
    mtx = broker.checkout("file://localhost:5672/file_name_1.csv?format=CSV")
    broker.release(mtx)
    print (to_df(broker.list("localhost:5672")))

print("end")


