from twisted.internet import protocol, reactor, defer, endpoints
import GlobalParams
from xml.dom import minidom
from twisted.protocols import basic
import datetime

class ICBCProtocol(protocol.Protocol):
    def connectionMade(self):
        #self.factory.numProtocols = self.factory.numProtocols + 1
        print "Connection to " + str(self.transport.getPeer().host) + ":" + str(self.transport.getPeer().port)
        ip = str(self.transport.getPeer().host)
        GlobalParams.AddOneClient(self, str(self.transport.getPeer().host))

    def connectionLost(self,reason):
        #self.factory.numProtocols = self.factory.numProtocols - 1
        GlobalParams.DelOneClient(str(self.transport.getPeer().host))

    def dataSend(self, data):
        print data
        self.transport.write(data)


    def dataReceived(self, data):
        print data
        queue = GlobalParams.getEventProcessThread()
        queue.put((str(self.transport.getPeer().host), data))

class ICBCFactory(protocol.ServerFactory):
    protocol = ICBCProtocol

def startTCPServerMoudule():
    ICBCEndpoint = endpoints.serverFromString(reactor, "tcp:8800")
    ICBCEndpoint.listen(ICBCFactory())
    reactor.run()

if __name__ == "__main__":
    startTCPServerMoudule





