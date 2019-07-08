
from io import StringIO
from pymongo import MongoClient
from arctic import Arctic
import logging
import pkgutil
logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
import pandas as pd

handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

logger = logging.getLogger(__name__)


dat = pkgutil.get_data('isharp.demo.arctic.data','msft.csv')

data= StringIO(str(dat,'utf-8'))

df = pd.read_csv(data)
logger.info ("loaded msft tickers")

client = MongoClient('localhost')
print(client.server_info())

arctic = Arctic('localhost')
logger.info ("started Arctic on localhost")
















