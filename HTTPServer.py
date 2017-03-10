# coding=utf-8
from twisted.web.resource import Resource
from twisted.internet import reactor, endpoints
from twisted.web import server
import GlobalParams
from MsgParserBox import MsgParser
from CreateSQL import SQLCluster
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
        logger.debug("Received register data: " + data)
        #save register info
        msgparser = MsgParser()
        sqlcluster = SQLCluster()
        deviceId, channels = msgparser.parseRegisterData(data)
        try:
            if channels == {}:
                #unregister device
                deviceId = sqlcluster.selectDeviceId(deviceId)
                sqlcluster.updateDeviceRegisterInfo(deviceId, 0)
                sqlcluster.delChannelRegisterInfo(deviceId)
                logger.info("Unregister device: " + str(deviceId))
                return '200'
            else:
                #register device
                deviceId = sqlcluster.selectDeviceId(deviceId)
                sqlcluster.updateDeviceRegisterInfo(deviceId, 1)
                for k, v in channels.items():
                    inputDeviceId = deviceId
                    channelno = k
                    channelip = v[0]
                    channelport = v[1]
                    channelname = v[2]
                    channeltype = v[3]
                    sqlcluster.insertChannelRegisterInfo(str(channelname), channelno, channeltype, channelip, inputDeviceId, channelport)
                logger.info("Register device: " + str(deviceId))
                return '200'
        except Exception, e:
            logger.error("Error occured!!!", exc_info=True)
            return '400'

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