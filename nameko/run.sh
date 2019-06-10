# run server
nameko run --config ./nameko/config.yaml isharp.broker_service.server:DataBrokerService

#invoke client
#nameko shell --config ./nameko/config.yaml
#


import sys
sys.path.insert(0,'.')
n.rpc.data_broker_service.checkout("file:///file_name_1.csv?format=CSV")
