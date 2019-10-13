from logging import getLogger

from nameko.standalone.rpc import StandaloneProxyBase
from nameko.rpc import ServiceProxy
from nameko.containers import WorkerContext

from nameko_proxy.reply_listener import StandaloneReplyListener

__all__ = ['StandaloneRpcProxy']

logger = getLogger()


class _StandaloneProxyBase:

    ServiceContainer = StandaloneProxyBase.ServiceContainer
    Dummy = StandaloneProxyBase.Dummy

    _proxy = None

    def __init__(self, config, context_data=None,
                 timeout=None, reply_listener_cls=StandaloneReplyListener):

        self.container = self.ServiceContainer(config)
        self.context_data = context_data  # type: dict
        self.context_data_hooks = []

        self._reply_listener = reply_listener_cls(
            timeout=timeout).bind(self.container)

    def register_context_hook(self, func: callable):
        self.context_data_hooks.append(func)

    def __enter__(self):
        return self.start()

    def __exit__(self, tpe, value, traceback):
        self.stop()

    def start(self):
        self._reply_listener.setup()
        return self._proxy

    def stop(self):
        self._reply_listener.stop()


class _ClusterProxy:
    def __init__(self, container, entrypoint, reply_listener, context_callback: callable):
        self._container = container
        self._entrypoint = entrypoint
        self._reply_listener = reply_listener
        self._context_callback = context_callback

    @property
    def _worker_ctx(self):
        return WorkerContext(
            self._container, service=None, entrypoint=self._entrypoint,
            data=self._context_callback())

    def __getattr__(self, name):
        return ServiceProxy(self._worker_ctx, name, self._reply_listener)


class StandaloneRpcProxy(_StandaloneProxyBase):
    def __init__(self, *args, **kwargs):
        super(StandaloneRpcProxy, self).__init__(*args, **kwargs)
        self._proxy = _ClusterProxy(
            self.container, self.Dummy, self._reply_listener, context_callback=self.get_context_data)

    def get_context_data(self) -> dict:
        if self.context_data or self.context_data_hooks:
            context_data = self.context_data.copy() if self.context_data else {}
            for hook in self.context_data_hooks:
                context_data.update(hook())
            return context_data
