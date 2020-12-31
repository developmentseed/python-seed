echo Waiting for Kafka to be ready..
cub kafka-ready -b broker:29092 1 20
kafka-topics --create --if-not-exists --zookeeper zookeeper:2181 --partitions 1 --replication-factor 1 --topic pol.tickers
kafka-topics --create --if-not-exists --zookeeper zookeeper:2181 --partitions 1 --replication-factor 1 --topic pol.tickers.windowed.secs
kafka-topics --create --if-not-exists --zookeeper zookeeper:2181 --partitions 1 --replication-factor 1 --topic pol.tickers.falttened
echo topics created OK
echo Waiting for queues to be created

curl -X POST http://connect:8083//connectors -d @rabbit-request.json --header  "Content-Type: application/json"


while :; do sleep 2073600; done
