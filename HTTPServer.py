from pprint import pprint
from twisted.application.internet import TCPServer
from twisted.application.service import Application
from twisted.web.resource import Resource
from twisted.web.server import Site
from twisted.internet import reactor, endpoints
from twisted.web import server
from MyQueue import queue
from TCPServerModule import ICBCFactory

class ICBCHTTP(Resource):
    def render_Get(self, request):
        return ''

    def render_POST(self, request):
        #pprint(request.__dict__)
        #newdata = request.content.getvalue()
        newdata = request.content.read()
        queue.put(newdata)
        return ''

def http_tcp():
    #http in reactor
    root = Resource()
    root.putChild("data", ICBCHTTP())
    endpoints.serverFromString(reactor, "tcp:8000").listen(server.Site(root))
    #tcp in reactor
    ICBCEndpoint = endpoints.serverFromString(reactor, "tcp:8800")
    ICBCEndpoint.listen(ICBCFactory())
    #start the reactor
    reactor.run()
    
    
if __name__ == '__main__':
    http_tcp()