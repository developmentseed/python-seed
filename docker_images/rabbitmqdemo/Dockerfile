#
# RabbitMQ Dockerfile
#
# https://github.com/dockerfile/rabbitmq
#

# Pull base image.
FROM ubuntu




#Install python
RUN apt-get update

RUN apt --yes update && apt --yes upgrade
RUN apt install --yes wget

RUN apt-get install --yes python3
RUN apt-get install --yes python3-pip

COPY ./requirements.txt .

#RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Add files.
ADD bin/rabbitmq-start /usr/local/bin/


# Install RabbitMQ.
RUN \
  wget -qO - https://www.rabbitmq.com/rabbitmq-signing-key-public.asc | apt-key add - && \
  echo "deb http://www.rabbitmq.com/debian/ testing main" > /etc/apt/sources.list.d/rabbitmq.list && \
  apt-get  --allow-unauthenticated update && \
  DEBIAN_FRONTEND=noninteractive apt-get install --allow-unauthenticated -y rabbitmq-server && \
  rm -rf /var/lib/apt/lists/* && \
  rabbitmq-plugins enable rabbitmq_management && \
  echo "[{rabbit, [{loopback_users, []}]}]." > /etc/rabbitmq/rabbitmq.config && \
  chmod +x /usr/local/bin/rabbitmq-start

# Define environment variables.
ENV RABBITMQ_LOG_BASE /data/log
ENV RABBITMQ_MNESIA_BASE /data/mnesia

# Define mount points.
VOLUME ["/data/log", "/data/mnesia"]

# Define working directory.
WORKDIR /data

# Expose ports.
EXPOSE 5672
EXPOSE 15672

# Define default command.
CMD ["/bin/bash"]

