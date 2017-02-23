from pprint import pprint
from twisted.application.internet import TCPServer
from twisted.application.service import Application
from twisted.web.resource import Resource
from twisted.web.server import Site
from twisted.internet import reactor, endpoints
from twisted.web import server
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

def http():
    root = Resource()
    root.putChild("data", ICBCHTTP())
    endpoints.serverFromString(reactor, "tcp:8000").listen(server.Site(root))
    reactor.run()

if __name__ == '__main__':
    http()