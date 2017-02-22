from twisted.internet import protocol, reactor, defer, endpoints
from twisted.protocols import basic
import datetime
from MsgParserBox import MsgParser
from MyQueue import queue


class ICBCProtocol(protocol.Protocol):

    def connectionMade(self):
        self.factory.numProtocols = self.factory.numProtocols + 1
        self.transport.write(
            "Welcome! There are currently %d open connections.\n" %
            (self.factory.numProtocols,))
    
    def connectionLost(self,reason):
        self.factory.numProtocols = self.factory.numProtocols - 1

    def dataReceived(self, xmldata):
        print queue.qsize()
        queue.put(xmldata)
        #parser = MsgParser()
        #dataList = parser.parse(xmldata)
        #for data in dataList:
        #    print data

        #self.transport.loseConnection()

        #now = datetime.datetime.now()
        
        #file = open("D:/tcp.txt",'a')
        #file.write(now.strftime('%Y-%m-%d %H:%M:%S')+' |  '+ xmldata)
        #file.write('\n')
        #file.close()

class ICBCFactory(protocol.ServerFactory):
    protocol = ICBCProtocol
    numProtocols=0  



def tw():
    ICBCEndpoint = endpoints.serverFromString(reactor, "tcp:8000")
    ICBCEndpoint.listen(ICBCFactory())
    reactor.run()

if __name__ == '__main__':
    tw()






