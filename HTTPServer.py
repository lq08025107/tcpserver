from twisted.web.resource import Resource
from twisted.internet import reactor, endpoints
from twisted.web import server
import GlobalParams
from LogModule import setup_logging
import logging

from TCPServer import ICBCFactory

setup_logging()
logger = logging.getLogger(__name__)


class ICBCHTTP(Resource):
    def render_Get(self, request):
        return ''

    def render_POST(self, request):
        queue = GlobalParams.getStoreProcessQueue()
        #newdata = request.content.getvalue()
        newdata = request.content.read()
        queue.put(newdata)
        logger.info("Received post request from host: " + str(request.client.host) + ".")
        return ''

def start_http():
    #http in reactor
    root = Resource()
    root.putChild("data", ICBCHTTP())
    endpoints.serverFromString(reactor, "tcp:8000").listen(server.Site(root))
    #tcp in reactor
    ICBCEndpoint = endpoints.serverFromString(reactor, "tcp:8800")
    ICBCEndpoint.listen(ICBCFactory())
    #start the reactor
    reactor.run(installSignalHandlers=0)
    
    
if __name__ == '__main__':
    start_http()