from twisted.web.resource import Resource
from twisted.internet import reactor, endpoints
from twisted.web import server
from HTTPServer import ICBCHTTP
from HTTPServer import RegisterHTTP
from threading import Thread
#from TCPServer import ICBCFactory
from TCPServerPack import ICBCFactory
import ConfigParser
from LogModule import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)

class TwistedProcessThread(Thread):
    def __init__(self):
        self.cp = ConfigParser.SafeConfigParser()
        self.cp.read('config\config.ini')
        self.tcp_port = str(self.cp.get('server', 'tcp_server_port'))
        self.http_port = str(self.cp.get('server', 'http_server_port'))
        Thread.__init__(self)

    def run(self):
        logger.info("Twisted " + self.getName() + " Start Running")
        # http in reactor
        root = Resource()
        root.putChild("data", ICBCHTTP())
        root.putChild("register", RegisterHTTP())
        endpoints.serverFromString(reactor, "tcp:" + self.http_port).listen(server.Site(root))
        logger.info("HTTP Server listen on port: " + self.http_port)
        # tcp in reactor
        ICBCEndpoint = endpoints.serverFromString(reactor, "tcp:" + self.tcp_port)
        ICBCEndpoint.listen(ICBCFactory())
        logger.info("TCP Server listen on port: " + self.tcp_port)
        # start the reactor
        logger.info("Reactor has started.")
        reactor.run(installSignalHandlers=0)



def start_reactor():
    cp = ConfigParser.SafeConfigParser()
    cp.read('config\config.ini')
    #http in reactor
    root = Resource()
    root.putChild("data", ICBCHTTP())
    endpoints.serverFromString(reactor, "tcp:" + str(cp.get('server', 'http_server_port'))).listen(server.Site(root))
    #tcp in reactor
    ICBCEndpoint = endpoints.serverFromString(reactor, "tcp:" + str(cp.get('server', 'tcp_server_port')))
    ICBCEndpoint.listen(ICBCFactory())
    #start the reactor
    logger.info("Reactor has started.")
    reactor.run(installSignalHandlers=0)


if __name__ == '__main__':
    start_reactor()