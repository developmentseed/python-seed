from logging import getLogger

import eventlet
from eventlet import event
from kombu import Connection
from kombu.messaging import Consumer
from kombu.mixins import ConsumerMixin
from nameko.amqp import verify_amqp_uri
from nameko.constants import (
    AMQP_URI_CONFIG_KEY, DEFAULT_SERIALIZER, SERIALIZER_CONFIG_KEY)

logger = getLogger()


class QueueConsumer(ConsumerMixin):

    PREFETCH_COUNT_CONFIG_KEY = 'PREFETCH_COUNT'
    DEFAULT_KOMBU_PREFETCH_COUNT = 10

    def __init__(self, timeout=None):
        self.timeout = timeout

        self.provider = None
        self.queue = None
        self.prefetch_count = None
        self.serializer = None
        self.accept = []

        self._managed_threads = []
        self._consumers_ready = event.Event()
        self._connection = None

    @property
    def amqp_uri(self):
        return self.provider.container.config[AMQP_URI_CONFIG_KEY]

    @property
    def connection(self):
        if not self._connection:
            self._connection = Connection(self.amqp_uri)
        return self._connection

    def register_provider(self, provider):
        logger.debug("QueueConsumer registering: %s", provider)
        self.provider = provider
        self.queue = provider.queue
        self.serializer = provider.container.config.get(SERIALIZER_CONFIG_KEY, DEFAULT_SERIALIZER)
        self.prefetch_count = self.provider.container.config.get(
            self.PREFETCH_COUNT_CONFIG_KEY, self.DEFAULT_KOMBU_PREFETCH_COUNT)
        self.accept = [self.serializer]

        verify_amqp_uri(provider.container.config[AMQP_URI_CONFIG_KEY])

        self.start()

    def start(self):
        logger.info("QueueConsumer starting...")
        gt = eventlet.spawn(self.run)
        self._managed_threads.append(gt)
        gt.link(self._handle_thread_exited)

        self._consumers_ready.wait()

    def _handle_thread_exited(self, gt):
        self._managed_threads.remove(gt)
        try:
            gt.wait()
        except Exception as error:
            logger.error("Managed thread end with error: %s", error)

            if not self._consumers_ready.ready():
                self._consumers_ready.send_exception(error)

    def on_consume_ready(self, connection, channel, consumers, **kwargs):
        if not self._consumers_ready.ready():
            self._consumers_ready.send(None)

    def on_connection_error(self, exc, interval):
        logger.warning(
            "Error connecting to broker at {} ({}).\n"
            "Retrying in {} seconds.".format(self.amqp_uri, exc, interval))

    def unregister_provider(self, _):
        if self._connection:
            self.connection.close()
        self.should_stop = True

    def get_consumers(self, _, channel):
        consumer = Consumer(channel, queues=[self.provider.queue], accept=self.accept,
                            no_ack=False, callbacks=[self.provider.handle_message])
        consumer.qos(prefetch_count=self.prefetch_count)
        return [consumer]

    @staticmethod
    def ack_message(msg):
        msg.ack()
