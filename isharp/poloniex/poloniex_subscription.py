from autobahn.twisted.wamp import ApplicationSession
from autobahn.twisted.wamp import ApplicationRunner
from twisted.internet.defer import inlineCallbacks



class PoloniexComponent(ApplicationSession):
    def onConnect(self):
        self.join(self.config.realm)

    @inlineCallbacks
    def onJoin(self, details):
        def onTicker(*args):
            print("Ticker event received:", args)

        try:
            yield self.subscribe(onTicker, 'ticker')
        except Exception as e:
            print("Could not subscribe to topic:", e)


def main():
    runner = ApplicationRunner("wss://api2.poloniex.com", "realm1")
    runner.run(PoloniexComponent)


if __name__ == "__main__":
    main()