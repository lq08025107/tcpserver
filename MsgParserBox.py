from xml.dom.minidom import parseString
class MsgParser(object):
    def parse(self, xmlcontent):
        dom = parseString(xmlcontent)
        nodeList = []
        AlarmTypeID = dom.getElementsByTagName("AlarmTypeID")[0].childNodes[0].nodeValue
        nodeList.append(AlarmTypeID)
        
        AlarmTime = dom.getElementsByTagName("AlarmTime")[0].childNodes[0].nodeValue
        nodeList.append(AlarmTime)

        Score = dom.getElementsByTagName("Score")[0].childNodes[0].nodeValue
        nodeList.append(Score)
        
        DeviceID = dom.getElementsByTagName("DeviceID")[0].childNodes[0].nodeValue
        nodeList.append(DeviceID)

        ChannelID = dom.getElementsByTagName("ChannelID")[0].childNodes[0].nodeValue
        nodeList.append(ChannelID)
        
        Procedure = dom.getElementsByTagName("Procedure")[0].childNodes[0].nodeValue
        nodeList.append(Procedure)

        PictureData = dom.getElementsByTagName("PictureData")[0].childNodes[0].nodeValue
        nodeList.append(PictureData)
        return nodeList
    def constr(self, nodeList):
        query = "INSERT INTO AlarmEvent(DeviceID, ChannelID, AlarmTime, AlarmType, Score, PictrueUrl, ProcedureData) VALUES ("\
                    + nodeList[3] +","+ nodeList[4]+"," + nodeList[1]+"," + nodeList[0]+"," + nodeList[2]+"," + nodeList[6]+"," + nodeList[5] +")"
        return query
def main():
    msgparser = MsgParser()
    xml = """<?xml version="1.0" encoding="UTF-8"?>
    <WarningData>
    <AlarmTypeID>1</AlarmTypeID>
    <AlarmTime>'2016-04-12 08:48:54.000'</AlarmTime>
    <Score>65.2</Score>
    <DeviceID>300</DeviceID>
    <ChannelID>3</ChannelID>
    <Procedure>'Closing(time,1) -> 4 -> Foot(time,1) -> 4 -> Face(time,1) -> 1 -> Foot(time,1)'
    </Procedure>
    <PictureData>'ftp:\\10.25.18.30\\foo\\bar\\something.jpg'</PictureData>
    </WarningData>
    """
    msgParser = MsgParser()
    dataList = msgParser.parse(xml)
    querytest = msgParser.constr(dataList)
    print querytest

if __name__ == '__main__':
    main()
        
        
