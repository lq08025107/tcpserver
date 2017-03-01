from twisted.web.resource import Resource
from twisted.internet import reactor, endpoints
from twisted.web import server
from HTTPServer import ICBCHTTP
#from TCPServer import ICBCFactory
from TCPServerPack import ICBCFactory
from LogModule import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)

def start_reactor():
    #http in reactor
    root = Resource()
    root.putChild("data", ICBCHTTP())
    endpoints.serverFromString(reactor, "tcp:8000").listen(server.Site(root))
    #tcp in reactor
    ICBCEndpoint = endpoints.serverFromString(reactor, "tcp:8800")
    ICBCEndpoint.listen(ICBCFactory())
    #start the reactor
    logger.info("Reactor has started.")
    reactor.run(installSignalHandlers=0)


if __name__ == '__main__':
    start_reactor()