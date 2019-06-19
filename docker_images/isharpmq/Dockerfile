FROM rabbitmq:3-management

# Define environment variables.
ENV RABBITMQ_USER user
ENV RABBITMQ_PASSWORD user

ADD init.sh /init.sh
EXPOSE 15672

ADD rabbitmq.conf /etc/rabbitmq/rabbitmq.config

# Define default command
CMD ["/init.sh"]