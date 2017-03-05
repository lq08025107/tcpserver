# -*- coding=utf-8 -*-
from CreateSQL import SQLCluster
from MsgParserBox import MsgParser
from utiltool.DBOperator import MSSQL
import GlobalParams

from LogModule import setup_logging

import logging
setup_logging()
logger = logging.getLogger(__name__)
class AlarmUtil:
    def __init__(self):
        self.ms = MSSQL()
        self.sqlcluster = SQLCluster()
    '''

    params: orgId, positionId, alarmId, dateArrId, timeArrId, alarmLevel
    alarmLevel:
        gentable = GenTable()
        gentable.query([DicOrgType,DicPosition,DicAlarmType,DicDateAttribute,DicTimeAttribute])
    '''

    def saveAlarmInfo(self, dictAlarmEvent):

        id = 1

        orgId = self.sqlCluster.deviceID2orgID(dictAlarmEvent['DeviceID'])
        positionId = self.sqlCluster.deviceID2position(dictAlarmEvent['DeviceID'])
        alarmId = dictAlarmEvent['AlarmType']
        dateArrId = dictAlarmEvent['DateAttribute']
        timeArrId = dictAlarmEvent['TimeAttribute']

        gentable = GlobalParams.GetGenTable()
        alarmLevel = gentable.query([orgId, positionId, alarmId, dateArrId, timeArrId])

        parser = MsgParser()
        # save as db
        insertsql = parser.constrAlarmEventSQL(dictAlarmEvent, alarmLevel)
        id = self.ms.executeAndGetId(insertsql)
        logger.info("Message has been inserted into db successfully, id: " + str(id))

        auSco = GlobalParams.GetAutoScoreInstance()
        auSco.reqQueue.put({'orgId': orgId, 'deviceId': dictAlarmEvent['DeviceID'], 'alarmId': alarmId, 'dateArrId': dateArrId, 'timeArrId': timeArrId, 'currentAlarmLevel': alarmLevel})



    def createPackage(self, orgId, level, isDeal = 0, isFinish = 0):
        #创建新包
        packageId = self.sqlcluster.createPackage(orgId, level, isDeal, isFinish)

        #更新AlarmEvent中的packageid
        self.sqlcluster.updateAlarmEvent(packageId, id)

        #通知客户端
        notice_queue = GlobalParams.getNoticeProcessQueue()
        notice_queue.put(packageId)
        return packageId

    def updatePackageInfo(self, packageId, id, level):
        #更新包信息
        self.sqlcluster.updatePackageLevel(packageId, level)

        #更新AlarmEvent中的packageid
        self.sqlcluster.updateAlarmEvent(packageId, id)

        #通知客户端
        notice_queue = GlobalParams.getNoticeProcessQueue()
        notice_queue.put(packageId)

    def getMsg(self):
        # 获取要结包的packageId
        auSco = GlobalParams.GetAutoScoreInstance()
        packageid = auSco.respQueue.get()
        self.sqlcluster.updatePackageFinishInfo(packageid)


    def endPackageByUser(self, packageId, userName, time, record):
        msg = {}
        auSco = GlobalParams.GetAutoScoreInstance()
        self.sqlcluster.updatePackageFinishInfoByUser(packageId, userName, time, record)
        orgId = self.sqlcluster.selectOrgIdByPackageId(packageId)
        msg['orgId'] = orgId
        msg['stop'] = 1
        auSco.reqQueue.put(msg)
        #auSco.reqQueue.put({'orgId': 1, 'stop': 1})

if __name__ == '__main__':
    pass

