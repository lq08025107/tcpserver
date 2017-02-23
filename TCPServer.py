from twisted.internet import protocol, reactor, defer, endpoints
from twisted.protocols import basic
import datetime
from MsgParserBox import MsgParser
from MyQueue import queue


class ICBCHTTP(Resource):
    def render_Get(self, request):
        return ''

    def render_POST(self, request):
        #pprint(request.__dict__)
        #newdata = request.content.getvalue()
        newdata = request.content.read()
        print newdata
        queue.put(newdata)
        return ''

class ICBCProtocol(protocol.Protocol):

    def connectionMade(self):
        self.factory.numProtocols = self.factory.numProtocols + 1
        
        print "Welcome! There are currently %d open connections.\n" % (self.factory.numProtocols,)
    
    def connectionLost(self,reason):
        print "lost a connection"
        self.factory.numProtocols = self.factory.numProtocols - 1
        

    def stringReceived(self, xmldata):
        print xmldata
        
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



def tcp():
    #TCP server
    ICBCEndpoint = endpoints.serverFromString(reactor, "tcp:8000")
    ICBCEndpoint.listen(ICBCFactory())
    reactor.run()


if __name__ == '__main__':
    tcp()






