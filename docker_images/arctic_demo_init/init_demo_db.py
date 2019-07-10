import yaml

from pymongo import MongoClient
from arctic import Arctic
from arctic import auth
import logging

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
import pandas as pd
import arctic.hooks
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger = logging.getLogger(__name__)


def load_data_file(file_name, ticker_name,arctic_library):
    df = pd.read_csv(file_name)
    logger.info("loading {} from file {}".format(ticker_name,file_name))
    arctic_library.write(ticker_name,df)


conf = yaml.load(open('arctic_demo.yaml','r'))
client = MongoClient('localhost')
m_host= conf['mongo_db']['host']
lib_name = conf['lib_name']
arctic.hooks._get_auth_hook = lambda *args, **kwargs: auth.Credential(database=m_host,user=conf['mongo_db']['user'],password=conf['mongo_db']['password'])
arctic = Arctic(m_host)
logger.info ("started Arctic on {}".format(m_host))

arctic.initialize_library(lib_name)
dat_files = conf['data_files']
for key,value in dat_files.items():
    load_data_file(value,key,arctic[lib_name])
























