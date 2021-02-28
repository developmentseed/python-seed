echo Waiting for Kafka to be ready..
cub kafka-ready -b broker:29092 1 20
kafka-topics --create --if-not-exists --zookeeper zookeeper:2181 --partitions 1 --replication-factor 1 --topic pol.tickers
kafka-topics --create --if-not-exists --zookeeper zookeeper:2181 --partitions 1 --replication-factor 1 --topic pol.tickers.windowed.secs
kafka-topics --create --if-not-exists --zookeeper zookeeper:2181 --partitions 1 --replication-factor 1 --topic pol.tickers.windowed.mins
kafka-topics --create --if-not-exists --zookeeper zookeeper:2181 --partitions 1 --replication-factor 1 --topic pol.tickers.1.min.snaps
kafka-topics --create --if-not-exists --zookeeper zookeeper:2181 --partitions 1 --replication-factor 1 --topic pol.tickers.flattened
echo topics created OK
echo Waiting for queues to be created

# wait for queues to be created.
sleep 20

curl -X POST http://connect:8083/connectors -d @rabbit_request.json --header  "Content-Type: application/json"

# wait for connectors to be established
sleep 20

curl  http://connect:8083/connectors


while :; do sleep 2073600; done
