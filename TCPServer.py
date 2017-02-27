from twisted.internet import protocol, reactor, defer, endpoints
import GlobalParams
from LogModule import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)

class ICBCProtocol(protocol.Protocol):
    def connectionMade(self):
        #self.factory.numProtocols = self.factory.numProtocols + 1
        ip = str(self.transport.getPeer().host)
        port = str(self.transport.getPeer().port)
        logger.info("Client " + ip + ":" + port + "connected.")

        GlobalParams.AddOneClient(self, ip)

    def connectionLost(self,reason):
        #self.factory.numProtocols = self.factory.numProtocols - 1
        logger.info("Client " + str(self.transport.getPeer().host) + ":" + str(self.transport.getPeer().port) + "disconnected.")
        GlobalParams.DelOneClient(str(self.transport.getPeer().host))

    def dataSend(self, data):
        self.transport.write(data)


    def dataReceived(self, data):
        queue = GlobalParams.getEventProcessThread()
        queue.put((str(self.transport.getPeer().host), data))

class ICBCFactory(protocol.ServerFactory):
    protocol = ICBCProtocol

def startTCPServer():
    ICBCEndpoint = endpoints.serverFromString(reactor, "tcp:8800")
    ICBCEndpoint.listen(ICBCFactory())
    reactor.run()

if __name__ == "__main__":
    startTCPServer()





