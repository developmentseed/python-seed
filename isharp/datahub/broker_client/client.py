
from isharp.datahub.broker_client.remote_proxy import BrokerConnectionPool
from  isharp.datahub.broker_client.client_utils import mtx_headers_as_dataframe as to_df
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

aws_rpc_host = "ec2-54-158-255-146.compute-1.amazonaws.com"
local_host = "localhost"
rpc_host = local_host
with BrokerConnectionPool() as broker:
    # broker.releaseAll()
    # mtx = broker.checkout("file://datahub:5672/file_name_1.csv?format=CSV")
    # print(mtx.content)
    # broker.release(mtx)
    # mtx = broker.checkout("file://datahub:5672/file_name_1.csv?format=CSV")
    # broker.release(mtx)
    # # print (to_df(broker.list("datahub:5672")))
    # # print(broker.peek("file://datahub:5672/file_name_1.csv?format=CSV"))
    for thisItem in broker.list('{}:5672'.format(rpc_host)):
        print (thisItem)

    broker.releaseAll()
    mtx = broker.checkout('arctic://{}:5672/YahooFinance/SPOT/FTSE/0500'.format(rpc_host))
    print (mtx.matrix_header.path)

    mtx = broker.checkout('arctic://{}:5672/InvestCo/CLOSING/SP/EOD'.format(rpc_host))
    print(mtx.matrix_header.path)


    # print(broker.peek('arctic://{}:5672/InvestCo/CLOSING/SP/EOD'.format(rpc_host)))
    #
    # print(broker.peek('arctic://{}:5672/InvestCo/CLOSING/SPX/EOD'.format(rpc_host)))







