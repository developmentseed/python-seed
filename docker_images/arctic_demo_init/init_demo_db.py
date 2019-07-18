import yaml

from pymongo import MongoClient
from arctic import Arctic
from arctic import auth
import logging
import expandvars

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

def toDate(str):
    return pd.to_datetime(str)

def env_substitution(dict_in):
    for this_key,this_value in dict_in.items():
        dict_in[this_key] = expandvars.expandvars(this_value)

def load_data_file(file_name, ticker_name,arctic_library):
    df = pd.read_csv(file_name,converters={0:toDate}, index_col=0)
    logger.info("loading {} from file {}".format(ticker_name,file_name))
    arctic_library.write(ticker_name,df)


conf = yaml.load(open('arctic_demo.yaml','r'))
env_substitution(conf['mongo_db'])

if expandvars.expandvars(conf['skip']):
    logger.info("skipping wihtout loading since skip parameter is not empty")
    quit()



m_host= conf['mongo_db']['host']
client = MongoClient(m_host)
lib_name = conf['lib_name']
arctic_connection = Arctic(m_host)
if conf['mongo_db']['user']:
    logger.info("Creating login hook for user {}".format(conf['mongo_db']['user']))
    arctic.hooks._get_auth_hook = lambda *args, **kwargs: auth.Credential(database=m_host,user=conf['mongo_db']['user'],password=conf['mongo_db']['password'])


logger.info ("started Arctic on {}".format(m_host))

arctic_connection.initialize_library(lib_name)
dat_files = conf['data_files']
for key,value in dat_files.items():
    load_data_file(value,key,arctic_connection[lib_name])
























