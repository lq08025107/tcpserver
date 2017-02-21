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

def main():
    msgparser = MsgParser()
    xml = """\
<?xml version="1.0" encoding="UTF-8"?>
<WarningData>
<AlarmTypeID>1</AlarmTypeID>
<AlarmTime>"201702211112"</AlarmTime>
<Score>65.2</Score>
<DeviceID>300</DeviceID>
<ChannelID>3</ChannelID>
<Procedure>"Closing(time,1) -> 4 -> Foot(time,1) -> 4 -> Face(time,1) -> 1 -> Foot(time,1)"</Procedure>
<PictureData>"ftp://10.25.18.30/foo/bar/something.jpg"</PictureData>
</WarningData>
"""
    msgParser = MsgParser()
    dataList = msgParser.parse(xml)
    for data in dataList:
        print data

if __name__ == '__main__':
    main()
        
        
