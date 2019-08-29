import yaml
import dataclasses
from pymongo import MongoClient
from arctic import Arctic
from arctic import auth
import logging
import expandvars
import numpy as np
import pandas as pd
import datetime
import random
from pymongo import MongoClient
logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger = logging.getLogger(__name__)







def env_substitution(dict_in):
    for this_key,this_value in dict_in.items():
        dict_in[this_key] = expandvars.expandvars(this_value)

conf = yaml.unsafe_load(open('arctic_demo.yaml','r'))
env_substitution(conf['mongo_db'])

if expandvars.expandvars(conf['skip']):
    logger.info("skipping wihtout loading since skip parameter is not empty")
    quit()



m_host= conf['mongo_db']['host']



client = MongoClient(m_host)


client.drop_database('arctic')






