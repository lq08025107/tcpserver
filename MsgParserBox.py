from xml.dom.minidom import parseString, parse
from xml.dom import minidom
from LogModule import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)
class MsgParser(object):
    def docparse(self):
        dom = parse("D:\\tcp.xml")
        nodeList = []
        AlarmTypeID = dom.getElementsByTagName("AlarmTypeID")[0].childNodes[0].nodeValue
        nodeList.append(AlarmTypeID)
        PictureData = dom.getElementsByTagName("PictureData")[0].childNodes[0].nodeValue
        nodeList.append(PictureData)
        return nodeList
    def parseAlarmEvent(self, xmlcontent):

        dom = parseString(xmlcontent)
        nodeList = {}
        AlarmTypeID = dom.getElementsByTagName("AlarmTypeID")[0].childNodes[0].nodeValue
        nodeList['AlarmType'] = AlarmTypeID
        
        AlarmTime = dom.getElementsByTagName("AlarmTime")[0].childNodes[0].nodeValue
        nodeList['AlarmTime'] = AlarmTime

        Score = dom.getElementsByTagName("Score")[0].childNodes[0].nodeValue
        nodeList['Score'] = Score
        
        DeviceID = dom.getElementsByTagName("DeviceID")[0].childNodes[0].nodeValue
        nodeList['DeviceID'] = DeviceID

        ChannelID = dom.getElementsByTagName("ChannelID")[0].childNodes[0].nodeValue
        nodeList['ChannelID'] = ChannelID
        
        Procedure = dom.getElementsByTagName("Procedure")[0].childNodes[0].nodeValue
        nodeList['Procedure'] = Procedure

        PictureData = dom.getElementsByTagName("PictureData")[0].childNodes[0].nodeValue
        nodeList['PictureData'] = PictureData

        DateAttribute = dom.getElementsByTagName("DateAttribute")[0].childNodes[0].nodeValue
        nodeList['DateAttribute'] = DateAttribute

        TimeAttribute = dom.getElementsByTagName("TimeAttribute")[0].childNodes[0].nodeValue
        nodeList['TimeAttribute'] = TimeAttribute
        return nodeList

    def parseRegisterData(self, xmlcontent):
        Channels = {}
        DeviceID = None
        try:
            xmlfile = minidom.parseString(xmlcontent)
            DeviceID = xmlfile.getElementsByTagName("DeviceID")[0].childNodes[0].nodeValue
            for channel in xmlfile.getElementsByTagName("Channel"):
                channel_id = channel.getAttribute("id")
                channel_ip = channel.data
                channel_port = channel.childNodes[1].data
                Channels[channel_id] = [channel_ip, channel_port]

        except Exception, e:
            logger.error("This is not a well formed xml.", exc_info=True)

        return DeviceID, Channels

    def constrAlarmEventSQL(self, nodeList):
        query = "INSERT INTO AlarmEvent(DeviceID, ChannelID, AlarmTime, AlarmType, Score, PictrueUrl, ProcedureData) VALUES ("\
                    + nodeList['DeviceID'] +","+ nodeList['ChannelID']+"," + "'" + nodeList['AlarmTime'] + "'"+ "," + nodeList['AlarmType']+"," + nodeList['Score'] \
                    +"," +"'"+ nodeList['PictureData']+"'"+"," + "'" +nodeList['Procedure']+"'" +")"
        print query
        return query
def main():
    msgparser = MsgParser()
    xml = """<?xml version="1.0" encoding="utf-8"?>
<WarningData>
<AlarmTypeID>1</AlarmTypeID>
<AlarmTime>2016-04-12 08:48:54.000</AlarmTime>
<Score>65.2</Score>
<DeviceID>1</DeviceID>
<ChannelID>1</ChannelID>
<DateAttribute>1</DateAttribute>
<TimeAttribute>1</TimeAttribute>
<Procedure>Closing(time,1) -> 4 -> Foot(time,1) -> 4 -> Face(time,1) -> 1 -> Foot(time,1)</Procedure>
<PictureData>ftp://10.25.18.30/foo/bar/something.jpg</PictureData>
</WarningData>
    """

    registerxml = """<?xml version="1.0" encoding="utf-8"?>
<RegisterData>
    <DeviceInfo>
		<DeviceID>1</DeviceID>
    </DeviceInfo>
    <Channels>
        <Channel id="1">

            <ChannelIP>10.25.18.9</ChannelIP>
            <ChannelPort>8080</ChannelPort>
        </Channel>
        <Channel id="2">
            <ChannelIP>10.25.18.9</ChannelIP>
            <ChannelPort>8080</ChannelPort>
        </Channel>
    </Channels>
</RegisterData>
"""
    msgParser = MsgParser()
    #dataList = msgParser.docparse()
    #dataList = msgParser.parseAlarmEvent(xml)
    #querytest = msgParser.constr(dataList)
    #print querytest
    #msgParser.constrAlarmEventSQL(dataList)
    deviceid, channels = msgParser.parseRegisterData(registerxml)
    print deviceid
    for channel in channels:
        print channel[0]


if __name__ == '__main__':
    main()

        
