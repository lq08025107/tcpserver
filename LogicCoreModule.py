# -*- coding=utf-8 -*-
from threading import Thread
import Queue
import time
import GlobalParams
from xml.dom import minidom
from utiltool.DBOperator import MSSQL
from LogModule import setup_logging
import logging
import sys

reload(sys)
sys.setdefaultencoding('utf8')

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
                #operateData = message[1].decode('GBK').encode('UTF-8')
                operateData = message[1]
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

        xmlstring = dom.toxml()

        return xmlstring

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
            RetCode = id
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
            logger.error("Error Type Number!! Please Check Interface Book!!!")


        return RetCode, RetInfo

    def event2record(self, id, procUserName, procTime, procRecord):
        ms = MSSQL()
        try:
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
            logger.info("%s process a message and write: %s" % (str(procUserName), str(procRecord)))

        except Exception, e:
            logger.error("There is no Message with id: " + str(id), exc_info=True)

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
                    logger.info("Send the message to client Already.")

        logger.info("Notice " + self.getName() + " Stop Run")

    def buildxml4client(self, id):

        impl = minidom.getDOMImplementation()
        dom = impl.createDocument(None, 'WarningIDs', None)
        root = dom.documentElement

        msg = dom.createElement('WarningID')
        data = dom.createTextNode(str(id))
        msg.appendChild(data)
        root.appendChild(msg)

        xmlstring = dom.toxml();
        return xmlstring

if __name__ == '__main__':

    ept = EventProcessThread()
    xmls = ept.buildXml('1', '101', 300, '')
    print xmls
    npt = NoticeProcessThread()
    xml = npt.buildxml4client(8)
    print xml
    


