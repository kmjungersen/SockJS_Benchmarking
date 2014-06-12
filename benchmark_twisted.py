from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor
from txsockjs.factory import SockJSFactory
from txsockjs.utils import broadcast

import time
import os


class TwistedChatConnection(Protocol):
    
    message_count = 0
    message_target = 100
    message_start_time = 0
    message_stop_time = 0
    setup_stop_time = 0
    teardown_start_time = 0
    summary = ''

    # def setup(self):
    #
    #     self.message_target = 1000

    def connectionMade(self):

        with open('data/setup_stop_time.txt', 'a+') as setup_stop_file:
            self.setup_stop_time = time.time()
            setup_stop_file.write(str(self.setup_stop_time) + '\n')

        if not hasattr(self.factory, "transports"):
            self.factory.transports = set()
        self.factory.transports.add(self.transport)

        with open('data/message_start_time.txt', 'a+') as message_start_file:
            self.message_start_time = time.time()
            message_start_file.write(str(self.message_start_time) + '\n')

    def dataReceived(self, data):

        broadcast(data, self.factory.transports)
        self.message_count += 1

        if self.message_count == self.message_target:
            reactor.stop()

    def connectionLost(self, reason=''):

        with open('data/message_stop_time.txt', 'a+') as message_stop_file:
            self.message_stop_time = time.time()
            message_stop_file.write(str(self.message_stop_time) + '\n')

        with open('data/teardown_start_time.txt', 'a+') as teardown_start_file:
            self.teardown_start_time = time.time()
            teardown_start_file.write(str(self.teardown_start_time) + '\n')

        #self.summarize()

    def summarize(self):

        self.summary += '=========================================\n'
        self.summary += 'twisted summary\n'
        self.summary += str(self.message_count)
        self.summary += ' total messages were sent/received in '
        self.summary += str(self.message_stop_time - self.message_start_time)
        self.summary += ' seconds.\n'
        self.summary += '=========================================\n'

        print self.summary

def server_setup(port):
    f = SockJSFactory(Factory.forProtocol(TwistedChatConnection))

    reactor.listenTCP(port, f)

    os.system('open static/index_twisted.html')

    reactor.run()

server_setup(8020)