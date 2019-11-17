
from isharp.datahub.broker_client.remote_proxy import BrokerConnectionPool
from  isharp.datahub.broker_client.client_utils import mtx_headers_as_dataframe as to_df
import logging
import json
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

aws_rpc_host = "isharpdemo"
local_host = "localhost"
rpc_host = aws_rpc_host
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

    broker.releaseAll()

    hist = broker.history('arctic://{}:5672/YahooFinance/SPOT/FTSE/0500'.format(rpc_host))

    hist = broker.history('arctic://{}:5672/isharp/AAPL'.format(rpc_host))
    # mtx = broker.view('arctic://{}:5672/InvestCo/CLOSING/SP/EOD'.format(rpc_host))





    # row_data = []
    # dict_array = mtx.content.to_dict(orient='records')
    # for idx, row in enumerate(dict_array):
    #     row["date"]=mtx.content.index[idx].strftime("%d %b %Y")
    #     row_data.append(row)
    #
    # column_headers = list(mtx.content)
    # column_headers.append("date")





    print ("finidhse")














