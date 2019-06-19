FROM rabbitmq:3-management

EXPOSE 15672

#ADD rabbitmq.conf /etc/rabbitmq/rabbitmq.config

RUN "echo [{rabbit, [{loopback_users, []}]}]." > /etc/rabbitmq/rabbitmq.config

