import sockjs.tornado
import tornado.web
import tornado.ioloop
import time
import webbrowser


class TornadoIndexHandler(tornado.web.RequestHandler):

    """regular http handler to serve the chatroom page"""
    def get(self):
        self.render('static/index.html')


class TornadoChatConnection(sockjs.tornado.SockJSConnection):

    """chat connection implementation"""
    # class level variable
    participants = set()
    message_count = 0
    message_target = 1000
    message_start_time = 0
    message_stop_time = 0
    setup_stop_time = 0
    teardown_start_time = 0
    summary = ''

    def setup(self):

        self.message_target = 1000

    def on_open(self, info):
        with open('data/setup_stop_time.txt', 'a+') as setup_stop_file:
            self.setup_stop_time = time.time()
            setup_stop_file.write(str(self.setup_stop_time) + '\n')

        # add client to the clients list
        self.participants.add(self)
        with open('data/message_start_time.txt', 'a+') as message_start_file:
            self.message_start_time = time.time()
            message_start_file.write(str(self.message_start_time) + '\n')

    def on_message(self, message):

        # broadcast message
        self.broadcast(self.participants, message)
        self.message_count += 1
        if self.message_count == self.message_target:
            self.close()

    def on_close(self):

        # remove client from the clients list and broadcast leave message
        with open('data/message_stop_time.txt', 'a+') as message_stop_file:
            self.message_stop_time = time.time()
            message_stop_file.write(str(self.message_stop_time) + '\n')

        with open('data/teardown_start_time.txt', 'a+') as teardown_start_file:
            self.teardown_start_time = time.time()
            teardown_start_file.write(str(self.teardown_start_time) + '\n')

        #self.summarize()

        tornado.ioloop.IOLoop.instance().stop()

    def summarize(self):

        self.summary += '=========================================\n'
        self.summary += 'tornado summary\n'
        self.summary += str(self.message_count)
        self.summary += ' total messages were sent/received in '
        self.summary += str(self.message_stop_time - self.message_start_time)
        self.summary += ' seconds.\n'
        self.summary += '=========================================\n'

        print self.summary


def server_setup(port):

    tornado_router = sockjs.tornado.SockJSRouter(TornadoChatConnection, '/chat')

    tornado_app = tornado.web.Application(
        [(r"/", TornadoIndexHandler)] + tornado_router.urls)

    tornado_app.listen(port)

    address = 'http://127.0.0.1:' + str(port)
    webbrowser.open_new_tab(address)

    tornado.ioloop.IOLoop.instance().start()

server_setup(8000)
