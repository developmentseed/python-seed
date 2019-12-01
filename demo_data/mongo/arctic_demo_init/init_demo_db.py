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
import sys
import isharp.datahub.core as dhubcore
from isharp.datahub.arctic_broker.broker_impl.arctic_storage_method import import_pandas
from isharp.datahub.arctic_broker.broker_impl import arctic_storage_method

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

empty_results = pd.DataFrame(
    columns=['Volume', 'L14', 'H14', '%K', '%D', 'Sell Entry', 'Sell Exit', 'Short', 'Buy Entry', 'Buy Exit', 'Long','Position', 'Market Returns', 'Strategy Returns'])

@dataclasses.dataclass(frozen=True)
class RandomMatrix(object):
    drift_pc: int
    step_size: float
    start_value : float
    start_date : str
    end_date : str
    time_slot_interval : str


    def to_df(self):
        index = pd.date_range(start=self.start_date, end=self.end_date)

        time_range = pd.date_range("00:00", "23:59", freq=self.time_slot_interval)
        time_slots = [d.strftime("%H%M") for d in time_range]
        time_slots.append('EOD')

        base_array = np.zeros((len(index), len(time_slots)))
        base_array[0].fill(self.start_value)

        for i in range(1, len(base_array)):
            prev_base_value = base_array[i - 1, 0]
            step_x = random.randint(0, 100) + self.drift_pc
            adj = abs(self.step_size * np.random.normal())
            direction = 1 if step_x > 50 else -1
            adj = adj * direction
            row = base_array[i]
            base_value = prev_base_value + adj
            row.fill(base_value)
            for i in range(1, len(row)):
                up = random.randint(0, 1)
                adj = 0.0009983 * np.random.normal()
                if not up:
                    adj = adj * -1
                row[i] = row[i - 1] + adj

        return  pd.DataFrame(data=base_array, index=index, columns=time_slots)


def toDate(str):
    return pd.to_datetime(str)

def env_substitution(dict_in):
    for this_key,this_value in dict_in.items():
        dict_in[this_key] = expandvars.expandvars(this_value)


def load_arctic_dataframe_with_versions(df, ticker_name, arctic_library,evaluations_library):
    df_len,df_width = df.shape
    base_df = df.iloc[:df_len-5]
    delta_df = df.iloc[df_len-5:]

    last_base_time = df.index[-1]
    commit_message = "Initial import for dataframe {}: Historical backfill up to {}".format(ticker_name,last_base_time)
    eval_commit_message = "Initial import for eval dataframe {}".format(ticker_name)
    eval_rev_info = dhubcore.RevisionInfo(who="demo_sys", what=eval_commit_message, when=last_base_time)
    rev_info = dhubcore.RevisionInfo(who="demo_sys", what=commit_message, when=last_base_time)
    arctic_storage_method.import_pandas(arctic_library,base_df,ticker_name,rev_info)

    arctic_storage_method.import_pandas(evaluations_library,empty_results,ticker_name,eval_rev_info)

    for index,row in delta_df.iterrows():
        stored_df = arctic_library.read(ticker_name,None).data
        insert_date = delta_df.index[-1]
        new_df = stored_df.append(row)
        commit_message = "Auto-feeed inserted data for  [{}]".format(ticker_name,insert_date)
        rev_info = dhubcore.RevisionInfo(who="auto-feed", when=insert_date,what=commit_message)
        arctic_storage_method._store_content(arctic_library,ticker_name,new_df,rev_info)


def load_data_file(file_name, ticker_name,arctic_library,eval_library):
    logger.info("loading {} from file {}".format(ticker_name, file_name))
    df = pd.read_csv(file_name,converters={0:toDate}, index_col=0)
    load_arctic_dataframe_with_versions(df,ticker_name,arctic_library,eval_library)



conf = yaml.load(open(sys.argv[1],'r'))
env_substitution(conf['mongo_db'])
env_substitution(conf['data_files'])

if expandvars.expandvars(conf['skip']):
    logger.info("skipping wihtout loading since skip parameter is not empty")
    quit()



m_host= conf['mongo_db']['host']
client = MongoClient(m_host)
lib_name = conf['lib_name']
evaluations_lib_name =  ("evaluations_{}".format(conf['lib_name']))

if conf['mongo_db']['user']:
    mongo_user = conf['mongo_db']['user']
    mongo_pwd = conf['mongo_db']['password']
    logger.info("Creating login hook for user {} pwd {} on mongo_host {}".format(mongo_user, mongo_pwd, m_host))
    arctic.hooks._get_auth_hook = lambda *args, **kwargs: auth.Credential(database=m_host,user=conf['mongo_db']['user'],password=conf['mongo_db']['password'])

arctic_connection = Arctic(m_host)

logger.info ("started Arctic on {}".format(m_host))

arctic_connection.initialize_library(lib_name)
arctic_connection.initialize_library(evaluations_lib_name)

dat_files = conf['data_files']
for key,value in dat_files.items():
    load_data_file(value,key,arctic_connection[lib_name],arctic_connection[evaluations_lib_name])




series = RandomMatrix(
drift_pc = 10,
step_size=0.01,
start_value=7,
start_date='1/1/2015',
end_date = '1/1/2019',
time_slot_interval = "15min"
)



lib_name = 'YahooFinance'

arctic_connection.initialize_library(lib_name)
import_pandas(arctic_connection[lib_name],series.to_df(),"SPOT.FTSE.0500",dhubcore.RevisionInfo(who="inital committer", what="initial commit", when = datetime.datetime.now()))


lib_name = 'InvestCo'
arctic_connection.initialize_library(lib_name)
arctic_connection[lib_name].write("CLOSING.SP.EOD", series.to_df())























