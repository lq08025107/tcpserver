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

        orgId = self.sqlcluster.deviceID2orgID(dictAlarmEvent['DeviceID'])
        orgType = self.sqlcluster.selectOrgTypeByOrgId(orgId)#Type
        positionId = self.sqlcluster.deviceID2position(dictAlarmEvent['DeviceID'])
        alarmId = int(dictAlarmEvent['AlarmType'])
        dateArrId = int(dictAlarmEvent['DateAttribute'])
        timeArrId = int(dictAlarmEvent['TimeAttribute'])

        gentable = GlobalParams.GetGenTable()
        alarmLevel = gentable.query([orgType, positionId, alarmId, dateArrId, timeArrId])

        parser = MsgParser()
        # save as db

        id = self.sqlcluster.insertAlarmEvent(dictAlarmEvent, alarmLevel)
        logger.info("Message has been inserted into db successfully, id: " + str(id))

        auSco = GlobalParams.GetAutoScoreInstance()
        auSco.reqQueue.put({'orgId': orgId, 'deviceId': dictAlarmEvent['DeviceID'], 'alarmId': alarmId, 'dateArrId': dateArrId, 'timeArrId': timeArrId, 'currentAlarmLevel': alarmLevel, 'id': id})
        logger.info("put message to process core")


    def createPackage(self, orgId, level, id, isDeal = 0, isFinish = 0):
        #创建新包
        packageId = self.sqlcluster.createPackage(orgId, level, isDeal, isFinish)

        #更新AlarmEvent中的packageid
        self.sqlcluster.updateAlarmEvent(packageId, id)

        #通知客户端
        notice_queue = GlobalParams.getNoticeProcessQueue()
        notice_queue.put(packageId)
        logger.info("create package: " + str(packageId))
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
        dict = auSco.respQueue.get()
        self.sqlcluster.updatePackageFinishInfo(dict['packageId'])


    def endPackageByUser(self, packageId, userName, time, record):
        msg = {}
        auSco = GlobalParams.GetAutoScoreInstance()
        #self.sqlcluster.updatePackageFinishInfoByUser(packageId, userName, time, record)
        orgId = self.sqlcluster.selectOrgIdByPackageId(packageId)
        msg['orgId'] = orgId
        msg['userName'] = userName
        msg['time'] = time
        msg['record'] = record
        msg['packageId'] = packageId
        msg['stop'] = 'End by client'
        auSco.reqQueue.put(msg)
        #auSco.reqQueue.put({'orgId': 1, 'stop': 1})

if __name__ == '__main__':
    pass

