import cyclone.web
from twisted.internet import reactor

import sockjs.cyclone
import time
import webbrowser

class CycloneIndexHandler(cyclone.web.RequestHandler):
    """ Serve the chat html page """
    def get(self):
        self.render('static/index.html')


class CycloneChatConnection(sockjs.cyclone.SockJSConnection):
    """ chat sockjs connection """

    participants = set()
    message_count = 0
    message_target = 100
    message_start_time = 0
    message_stop_time = 0
    setup_stop_time = 0
    teardown_start_time = 0
    summary = ''

    def setup(self):

        self.message_target = 1000

    def connectionMade(self, info):
        with open('data/setup_stop_time.txt', 'a+') as setup_stop_file:
            self.setup_stop_time = time.time()
            setup_stop_file.write(str(self.setup_stop_time) + '\n')

        self.participants.add(self)

        with open('data/message_start_time.txt', 'a+') as message_start_file:
            self.message_start_time = time.time()
            message_start_file.write(str(self.message_start_time) + '\n')


    def messageReceived(self, message):

        self.broadcast(self.participants, message)
        self.message_count += 1

        if self.message_count == self.message_target:
            self.close()

    def connectionLost(self):

        with open('data/message_stop_time.txt', 'a+') as message_stop_file:
            self.message_stop_time = time.time()
            message_stop_file.write(str(self.message_stop_time) + '\n')

        with open('data/teardown_start_time.txt', 'a+') as teardown_start_file:
            self.teardown_start_time = time.time()
            teardown_start_file.write(str(self.teardown_start_time) + '\n')

        #self.summarize()

        reactor.stop()

    def summarize(self):

        self.summary += '=========================================\n'
        self.summary += 'Cyclone Summary\n'
        self.summary += str(self.message_count)
        self.summary += ' total messages were sent/received in '
        self.summary += str(self.message_stop_time - self.message_start_time)
        self.summary += ' seconds.\n'
        self.summary += '=========================================\n'

        print self.summary


def server_setup(port):

    cyclone_router = sockjs.cyclone.SockJSRouter(CycloneChatConnection, '/chat')

    app = cyclone.web.Application(
        [(r"/", CycloneIndexHandler)] + cyclone_router.urls)

    reactor.listenTCP(port, app)

    address = 'http://127.0.0.1:' + str(port)
    webbrowser.open_new_tab(address)

    reactor.run()

server_setup(8010)