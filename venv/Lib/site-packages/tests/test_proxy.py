import eventlet
from nameko.rpc import rpc
from nameko.exceptions import deserialize_to_instance
from nameko.containers import ServiceContainer

from nameko_proxy import StandaloneRpcProxy


CONFIG = {
    'AMQP_URI': 'pyamqp://guest:guest@127.0.0.1'
}


@deserialize_to_instance
class TestError(Exception):
    def __init__(self, msg):
        self.msg = msg


class FooService(object):
    name = 'foo_service'

    @rpc
    def test(self, val):
        return val

    @rpc
    def error(self, msg):
        raise TestError(msg)

    @rpc
    def sleep(self, seconds=0):
        eventlet.sleep(seconds)
        return seconds


def test_rpc_proxy():
    container = ServiceContainer(FooService, CONFIG)
    container.start()

    with StandaloneRpcProxy(CONFIG) as proxy:
        assert proxy.foo_service.test("test") == "test"

        msg = "Error occurred"
        try:
            proxy.foo_service.error(msg)
        except TestError as error:
            assert str(error) == msg


def test_async_calls():
    container = ServiceContainer(FooService, CONFIG)
    container.start()

    with StandaloneRpcProxy(CONFIG) as proxy:
        resp1 = proxy.foo_service.test.call_async(1)
        resp2 = proxy.foo_service.sleep.call_async(2)
        resp3 = proxy.foo_service.test.call_async(3)
        resp4 = proxy.foo_service.test.call_async(4)
        resp5 = proxy.foo_service.test.call_async(5)
        assert resp2.result() == 2
        assert resp3.result() == 3
        assert resp1.result() == 1
        assert resp4.result() == 4
        assert resp5.result() == 5
