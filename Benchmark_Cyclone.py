import cyclone.web
from twisted.internet import reactor

import sockjs.cyclone
import time
import webbrowser

class CycloneIndexHandler(cyclone.web.RequestHandler):
    """ Serve the chat html page """
    def get(self):
        self.render('Static/index.html')


class CycloneChatConnection(sockjs.cyclone.SockJSConnection):
    """ Chat sockjs connection """
    participants = set()
    MessageCount = 0
    MessageTarget = 10
    MessageStartTime = 0
    MessageStopTime = 0
    SetupStopTime = 0
    TeardownStartTime = 0
    Summary = ''

    def connectionMade(self, info):
        with open('Data/SetupStopTime.txt', 'a+') as SetupStopFile:
            self.SetupStopTime = time.time()
            SetupStopFile.write(str(self.SetupStopTime) + '\n')

        self.participants.add(self)

        with open('Data/MessageStartTime.txt', 'a+') as MessageStartFile:
            self.MessageStartTime = time.time()
            MessageStartFile.write(str(self.MessageStartTime) + '\n')


    def messageReceived(self, message):

        self.broadcast(self.participants, message)
        self.MessageCount += 1
        if self.MessageCount == self.MessageTarget:
            self.close()

    def connectionLost(self):

        with open('Data/MessageStopTime.txt', 'a+') as MessageStopFile:
            self.MessageStopTime = time.time()
            MessageStopFile.write(str(self.MessageStopTime) + '\n')

        # self.Summary += '=========================================\n'
        # self.Summary += 'CYCLONE SUMMARY\n'
        # self.Summary += str(self.MessageCount)
        # self.Summary += ' total messages were sent/received in '
        # self.Summary += str(self.MessageStopTime - self.MessageStartTime)
        # self.Summary += ' seconds.\n'
        # self.Summary += '=========================================\n'

        with open('Data/TeardownStartTime.txt', 'a+') as TeardownStartFile:
            self.TeardownStartTime = time.time()
            TeardownStartFile.write(str(self.TeardownStartTime) + '\n')

        #print self.Summary

        self.participants.remove(self)
        reactor.stop()


def ServerSetup(port):

    CycloneRouter = sockjs.cyclone.SockJSRouter(CycloneChatConnection, '/chat')

    app = cyclone.web.Application( [ (r"/", CycloneIndexHandler) ] +
                                   CycloneRouter.urls )
    reactor.listenTCP(port, app)
    address = 'http://127.0.0.1:' + str(port)
    webbrowser.open_new_tab(address)
    reactor.run()

ServerSetup(8010)