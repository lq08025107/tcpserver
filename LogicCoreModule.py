# -*- coding=utf-8 -*-
from threading import Thread
import Queue
import time
import GlobalParams
from xml.dom import minidom
from utiltool.DBOperator import MSSQL
from LogModule import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)



# 事件处理线程，主要处理前台对后台的操作事件
# 不与接收线程绑定，可作为线程池使用
class EventProcessThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.ProcessQueue = Queue.Queue()
        self.IsRunning = True

    def StopThread(self):
        self.IsRunning = False

    def run(self):
        logger.info("Event " + self.getName() + " Start Running")

        while self.IsRunning:
            while self.ProcessQueue.not_empty:
                message = self.ProcessQueue.get()
                clientID = message[0]
                operateData = message[1].decode('GBK').encode('UTF-8')
                OperaterID, Type, params = self.parseXml(operateData)
                RetCode, RetInfo = self.process(Type, params)
                RetMessage = self.buildXml(OperaterID, Type, RetCode, RetInfo)

                client = GlobalParams.GetOneClient(clientID)
                if client != None:
                    client.dataSend(RetMessage)

        logger.info("Event " + self.getName() + " Stop Run")

    def parseXml(self, data):
        Type = -1
        Params = {}
        OperaterId = None
        try:
            xmlfile = minidom.parseString(data)
            OperaterId = xmlfile.getElementsByTagName("Operator")[0].getAttribute("id")
            Type = int(xmlfile.getElementsByTagName("Type")[0].firstChild.data)
            for param in xmlfile.getElementsByTagName("Param"):
                param_id = param.getAttribute("id")
                param_value = param.firstChild.data
                Params[param_id] = param_value

        except Exception, e:
            logger.error("This is not a well formed xml.", exc_info=True)

        return OperaterId, Type, Params

    def buildXml(self, operaterID, type, retCode, retInfo):

        impl = minidom.getDOMImplementation()
        dom = impl.createDocument(None, 'WarningData', None)
        root = dom.documentElement

        root.setAttribute("id",str(operaterID))  # 增加属性

        msg = dom.createElement('Type')
        alarmTypeId = dom.createTextNode(str(type))
        msg.appendChild(alarmTypeId)
        root.appendChild(msg)

        msg = dom.createElement('RetCode')
        alarmTypeId = dom.createTextNode(str(retCode))
        msg.appendChild(alarmTypeId)
        root.appendChild(msg)

        if retInfo != None and len(retInfo) >= 1:
            msg = dom.createElement('RetInfos')
            for i in retInfo:
                msg1 = dom.createElement('RetInfo')
                msg1.setAttribute("id", str(i[0]))
                msg1.appendChild(dom.createTextNode(str(i[1])))
                msg.appendChild(msg1)

            root.appendChild(msg)

        f = open('./Xml/des.xml', 'w')
        dom.writexml(f, addindent='  ', newl='\n')
        f.close()
        retXml = "Result Message"

        oldXmlFile = open('./Xml/des.xml')
        oldXml = oldXmlFile.read()
        oldXmlFile.close()

        return oldXml

    def process(self, type, params):
        RetCode = -1
        RetInfo = None

        if type == 100:
            # 执行操作1=============
            #print str(params)
            id = params['1'].encode("utf-8")
            user =  params['2'].encode("utf-8")
            time = params['3'].encode("utf-8")
            operation = params['4'].encode("utf-8")
            self.event2record(id, user, time, operation)
            RetCode = 0
            # RetInfo = [(1, "11111"), (2, "22222")]
        elif type == 102:
            # 执行操作1=============
            print str(params)
        elif type == 103:
            # 执行操作1=============
            print str(params)
        elif type == 104:
            # 执行操作1=============
            print str(params)
        elif type == 105:
            # 执行操作1=============
            print str(params)
        else:
            logger.error("Error Type Number!! Please Chack Interface Book!!!", exc_info=True)


        return RetCode, RetInfo

    def event2record(self, id, procUserName, procTime, procRecord):
        ms = MSSQL()
        selectsql = "SELECT OrgID, DeviceID, DeviceName, ChannelID, AlarmTime, AlarmType, Score, PictrueUrl, \
        ProcedureData FROM AlarmEvent where ID=" + str(id)
        resList = ms.ExecQuery(selectsql)[0]
        insertsql = "INSERT INTO AlarmEventRecord (OrgID, DeviceID, AlarmTime, AlarmType, ChannelID, Score, PictrueUrl, ProcUserName," \
                    "ProcTime, ProcRecord, ProcedureData) VALUES (" + "NULL" + "," + str(
            resList["DeviceID"]) + "," + "'" + str(resList["AlarmTime"]) + "'" + "," + str(resList["AlarmType"]) \
                    + "," + str(resList["ChannelID"]) + "," + str(resList["Score"]) + "," + "'" + str(
            resList["PictrueUrl"]) + "'" \
                    + "," + "'" + str(procUserName) + "'" + "," + "'" + str(procTime) + "'" + "," + "'" + str(
            procRecord) + "'" + "," + "'" + str(resList["ProcedureData"]) + "'" + ")"
        deletesql = "DELETE FROM AlarmEvent where ID=" + str(id)

        ms.ExecMove(id, insertsql, deletesql)
        logger.info("%s process a message and write: %s" % (procUserName, procRecord))

class NoticeProcessThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.NoticeQueue = Queue.Queue()
        self.IsRunning = True

    def StopThread(self):
        self.IsRunning = False

    def run(self):
        logger.info("Notice " + self.getName() + " Start Running")
        while self.IsRunning:
            while not self.NoticeQueue.empty():
                data = self.NoticeQueue.get()
                xmlstring = self.buildxml4client(str(data))
                allClient = GlobalParams.GetAllClient()
                for client in allClient.values():
                    client.dataSend(xmlstring)

        logger.info("Notice " + self.getName() + " Stop Run")

    def buildxml4client(self, id):

        impl = minidom.getDOMImplementation()
        dom = impl.createDocument(None, 'WarningIDs', None)
        root = dom.documentElement

        msg = dom.createElement('WarningID')
        data = dom.createTextNode(str(id))
        msg.appendChild(data)
        root.appendChild(msg)

        f = open('./Xml/4client.xml', 'w')
        dom.writexml(f, addindent='  ', newl='\n')
        f.close()
        retXml = "Result Message"

        oldXmlFile = open('./Xml/des.xml')
        oldXml = oldXmlFile.read()
        oldXmlFile.close()

        return oldXml

if __name__ == '__main__':


    npt = NoticeProcessThread()
    npt.buildxml4client(8)
    


