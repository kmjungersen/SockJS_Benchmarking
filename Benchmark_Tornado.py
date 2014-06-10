'''Simple benchmarking program that will setup a connection, send X number
of messages, and then report how long it took'''

import sockjs.tornado
import tornado.web
import tornado.ioloop
import time
import webbrowser


class TornadoIndexHandler(tornado.web.RequestHandler):

    """Regular HTTP handler to serve the chatroom page"""
    def get(self):
        self.render('static/index.html')


class TornadoChatConnection(sockjs.tornado.SockJSConnection):

    """Chat connection implementation"""
    # Class level variable
    participants = set()
    MessageCount = 0
    MessageTarget = 10000
    MessageStartTime = 0
    MessageStopTime = 0
    Summary = ''

    def on_open(self, info):

        # Add client to the clients list
        self.participants.add(self)
        self.MessageStartTime = time.time()


    def on_message(self, message):

        # Broadcast message
        self.broadcast(self.participants, message)
        self.MessageCount += 1
        if self.MessageCount == self.MessageTarget:
            self.close()
            tornado.ioloop.IOLoop.instance().stop()

    def on_close(self):

        # Remove client from the clients list and broadcast leave message
        self.MessageStopTime = time.time()

        self.Summary += '=========================================\n'
        self.Summary += 'TORNADO SUMMARY\n'
        self.Summary += str(self.MessageCount)
        self.Summary += ' total messages were sent/received in '
        self.Summary += str(self.MessageStopTime - self.MessageStartTime)
        self.Summary += ' seconds.\n'
        self.Summary += '=========================================\n'

        print self.Summary

        tornado.ioloop.IOLoop.instance().stop()

        self.participants.remove(self)


def ServerSetup(port):

    # 1. Create chat router
    TornadoRouter = sockjs.tornado.SockJSRouter(TornadoChatConnection, '/chat')

    # 2. Create Tornado application
    tornado_app = tornado.web.Application(
            [(r"/", TornadoIndexHandler)] + TornadoRouter.urls
    )

    # 3. Make Tornado app listen on port specified in benchmark program
    tornado_app.listen(port)

    address = 'http://127.0.0.1:' + str(port)
    webbrowser.open_new_tab(address)

    # 4. Start IOLoop
    tornado.ioloop.IOLoop.instance().start()


    #return TornadoChatConnection.Summary

#if __name__ == '__main__':
#ServerSetup(8000)
