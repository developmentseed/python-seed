from logging import getLogger

from flask import current_app

from nameko_proxy import StandaloneRpcProxy

logger = getLogger()

EXTENSION_NAME = 'nameko_proxy'


class _NamekoProxyState:

    def __init__(self, proxy):
        self.proxy = proxy
        self.connection = None


def get_state(app) -> _NamekoProxyState:
    assert EXTENSION_NAME in app.extensions, \
        'The nameko_proxy extension was not registered to the current ' \
        'application. Please make sure to call init_app() first.'
    return app.extensions[EXTENSION_NAME]


class Config(dict):
    @classmethod
    def from_flask_config(cls, config):
        return cls({key[len('NAMEKO_'):]: val for key, val in config.items() if key.startswith('NAMEKO_')})

    def __getitem__(self, item):
        return super().__getitem__(item.upper())

    def get(self, k, default):
        return super().get(k.upper(), default)


class FlaskNamekoProxy:

    context_data = None
    context_data_hooks = []
    config = None

    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app, context_data=None):
        self.context_data = context_data
        self.config = Config.from_flask_config(app.config)

        app.extensions[EXTENSION_NAME] = _NamekoProxyState(self.get_proxy())

    def register_context_hook(self, func: callable):
        self.context_data_hooks.append(func)

    def __getattr__(self, name):
        if name not in vars(FlaskNamekoProxy):
            return getattr(self.connection, name)
        return getattr(self, name)

    @property
    def connection(self):
        state = get_state(current_app)

        if state.connection is None:
            state.connection = state.proxy.start()

        return state.connection

    def get_proxy(self):
        nameko_proxy = StandaloneRpcProxy(
            self.config,
            context_data=self.context_data,
            timeout=self.config.get('RPC_TIMEOUT', None),
        )

        for hook in self.context_data_hooks:
            nameko_proxy.register_context_hook(hook)

        return nameko_proxy
