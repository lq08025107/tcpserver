from twisted.web.resource import Resource
from twisted.internet import reactor, endpoints
from twisted.web import server
from HTTPServer import ICBCHTTP
from threading import Thread
#from TCPServer import ICBCFactory
from TCPServerPack import ICBCFactory
from config import ServerConfig
from LogModule import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)

class TwistedProcessThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        logger.info("Twisted " + self.getName() + " Start Running")
        # http in reactor
        root = Resource()
        root.putChild("data", ICBCHTTP())
        endpoints.serverFromString(reactor, "tcp:" + str(ServerConfig.HTTPSERVERPORT)).listen(server.Site(root))
        logger.info("HTTP Server listen on port: " + str(ServerConfig.HTTPSERVERPORT))
        # tcp in reactor
        ICBCEndpoint = endpoints.serverFromString(reactor, "tcp:" + str(ServerConfig.TCPSERVERPORT))
        ICBCEndpoint.listen(ICBCFactory())
        logger.info("TCP Server listen on port: " + str(ServerConfig.TCPSERVERPORT))
        # start the reactor
        logger.info("Reactor has started.")
        reactor.run(installSignalHandlers=0)
        logger.info("Store " + self.getName() + " Stop Run")


def start_reactor():
    #http in reactor
    root = Resource()
    root.putChild("data", ICBCHTTP())
    endpoints.serverFromString(reactor, "tcp:" + str(ServerConfig.HTTPSERVERPORT)).listen(server.Site(root))
    #tcp in reactor
    ICBCEndpoint = endpoints.serverFromString(reactor, "tcp:" + str(ServerConfig.TCPSERVERPORT))
    ICBCEndpoint.listen(ICBCFactory())
    #start the reactor
    logger.info("Reactor has started.")
    reactor.run(installSignalHandlers=0)


if __name__ == '__main__':
    start_reactor()