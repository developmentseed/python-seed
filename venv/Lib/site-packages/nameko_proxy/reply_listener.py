from nameko.rpc import ReplyListener

from nameko_proxy.queue_consumer import QueueConsumer

__all__ = ['StandaloneReplyListener']


class StandaloneReplyListener(ReplyListener):

    queue_consumer = None

    def __init__(self, timeout=None):
        self.queue_consumer = QueueConsumer(timeout)
        super(StandaloneReplyListener, self).__init__()
