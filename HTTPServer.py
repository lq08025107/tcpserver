from twisted.web.resource import Resource
from twisted.internet import reactor, endpoints
from twisted.web import server
import GlobalParams
from LogModule import setup_logging
import logging

from TCPServer import ICBCFactory

setup_logging()
logger = logging.getLogger(__name__)

#Site: the object which associates a listening server port with the HTTP implementation
#Resource: a convenient base class to use when defining custom pages
#reactor: the object which implements the Twisted main loop

class ICBCHTTP(Resource):
    def render_GET(self, request):
        logger.info("Received get request from host: " + str(request.client.host) + ".")
        return 'Hello World! I am the Server for ICBC!'

    def render_POST(self, request):
        queue = GlobalParams.getStoreProcessQueue()
        #newdata = request.content.getvalue()
        newdata = request.content.read()
        queue.put(newdata)
        logger.info("Received post request from host: " + str(request.client.host) + ".")
        return ''

class RegisterHTTP(Resource):
    def render_GET(self, request):
        return 'Hello World! I am the Register Server for ICBC!'
    def render_POST(self,request):
        logger.info("Received post register request from host: " + str(request.client.host) + ".")
        data = request.content.read()
        logger.info("Received register data: " + data)
        #save register info

        return '200'

def start_http():
    #http in reactor
    root = Resource()
    root.putChild("register", RegisterHTTP())
    root.putChild("data", ICBCHTTP())

    endpoints.serverFromString(reactor, "tcp:8000").listen(server.Site(root))
    #tcp in reactor
    ICBCEndpoint = endpoints.serverFromString(reactor, "tcp:8800")
    ICBCEndpoint.listen(ICBCFactory())
    #start the reactor
    reactor.run(installSignalHandlers=0)
    
    
if __name__ == '__main__':
    start_http()