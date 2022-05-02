from isharp.datahub.broker_client.remote_proxy import BrokerConnectionPool
from arctic import Arctic
from isharp.datahub.arctic_broker.broker_impl.arctic_data_broker import ArcticBroker
from isharp.datahub.arctic_broker.broker_impl.arctic_storage_method import ArcticStorageMethod

# mongo_location = 'daphne174'
# print("setting up arctic broker against host {}".format(mongo_location))
# arctic = Arctic(mongo_location)
# broker =  ArcticBroker(arctic)
#
# node = broker.dir("")
# print(node)

with  BrokerConnectionPool() as pool:
    # pool.list("daphne174")
    # node = pool.dir("Poloniex/snaps/BTC_EOS/1630/lastTradePrice","daphne174")
    node = pool.dir("Poloniex/snaps/BTC_EOS", "daphne174")
    print(node)


