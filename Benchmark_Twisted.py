from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor
from txsockjs.factory import SockJSFactory, SockJSMultiFactory
from txsockjs.utils import broadcast

import time
import os


class TwistedChatConnection(Protocol):
    MessageCount = 0
    MessageTarget = 10000
    MessageStartTime = 0
    MessageStopTime = 0
    Summary = ''

    def connectionMade(self):
        if not hasattr(self.factory, "transports"):
            self.factory.transports = set()
        self.factory.transports.add(self.transport)
        self.MessageStartTime = time.time()

    def dataReceived(self, data):
        broadcast(data, self.factory.transports)
        self.MessageCount += 1
        if self.MessageCount == self.MessageTarget:
            reactor.stop()

    def connectionLost(self, reason=''):
        self.MessageStopTime = time.time()

        self.Summary += '=========================================\n'
        self.Summary += 'TWISTED SUMMARY\n'
        self.Summary += str(self.MessageCount)
        self.Summary += ' total messages were sent/received in '
        self.Summary += str(self.MessageStopTime - self.MessageStartTime)
        self.Summary += ' seconds.\n'
        self.Summary += '=========================================\n'

        print self.Summary

def ServerSetup(port):
    f = SockJSFactory(Factory.forProtocol(TwistedChatConnection))

    reactor.listenTCP(port, f)

    os.system('open /Users/kurtisjungersen/COS/NotificationCenterFiles/'
              'SockJS_Testing/benchmarking/Static/index_Twisted.html')

    reactor.run()

#ServerSetup(8020)