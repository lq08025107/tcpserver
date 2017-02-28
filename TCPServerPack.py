from twisted.internet import protocol, reactor, defer, endpoints
import GlobalParams
import struct
from LogModule import setup_logging
import logging
from PackModule import packData
setup_logging()
logger = logging.getLogger(__name__)

class ICBCProtocol(protocol.Protocol):
    _data_buffer = bytes()
    def connectionMade(self):
        #self.factory.numProtocols = self.factory.numProtocols + 1
        ip = str(self.transport.getPeer().host)
        port = str(self.transport.getPeer().port)
        logger.info("Client " + ip + ":" + port + " connected.")

        GlobalParams.AddOneClient(self, ip)

    def connectionLost(self,reason):
        #self.factory.numProtocols = self.factory.numProtocols - 1
        logger.info("Client " + str(self.transport.getPeer().host) + ":" + str(self.transport.getPeer().port) + " disconnected.")
        GlobalParams.DelOneClient(str(self.transport.getPeer().host))

    def dataSend(self, data):
        data = packData(data)
        self.transport.write(data)


    def dataReceived(self, data):
        self._data_buffer += data
        headerSize = 12
        while True:
            if len(self._data_buffer) < headerSize:
                return

            headPack = struct.unpack('!3I', self._data_buffer[:headerSize])
            bodySize = headPack[1]

            if len(self._data_buffer) < headerSize + bodySize:
                return

            body = self._data_buffer[headerSize:headerSize + bodySize]

            self.dataSend(body)
            queue = GlobalParams.getEventProcessThread()
            queue.put((str(self.transport.getPeer().host), data))

            self._data_buffer = self._data_buffer[headerSize + bodySize:]


class ICBCFactory(protocol.ServerFactory):
    protocol = ICBCProtocol

def startTCPServer():
    ICBCEndpoint = endpoints.serverFromString(reactor, "tcp:8800")
    ICBCEndpoint.listen(ICBCFactory())
    reactor.run()

if __name__ == "__main__":
    startTCPServer()





