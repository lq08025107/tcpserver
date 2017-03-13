# -*- coding=utf-8 -*-
from LogModule import setup_logging
from utiltool.DBOperator import MSSQL

import logging

class SQLCluster():
    def __init__(self, choice = 'd'):
        if choice == 'd':
            self.ms = MSSQL()
        else:
            self.ms = MSSQL(choice)

    def insertAlarmEvent(self, nodeList, alarmLevel):

        sql = "INSERT INTO AlarmEvent(DeviceID, ChannelID, AlarmTime, AlarmType, Score, PictrueUrl, ProcedureData, AlarmLevel) VALUES ("\
                    + nodeList['DeviceID'] +","+ nodeList['ChannelID']+"," + "'" + nodeList['AlarmTime'] + "'"+ "," + nodeList['AlarmType']+"," + nodeList['Score'] \
                    +"," +"'"+ nodeList['PictureData']+"'"+"," + "'" +nodeList['Procedure']+"'" + "," + str(alarmLevel) +")"

        return self.ms.executeAndGetId(sql)
    #根据设备id查询组织id
    def deviceID2orgID(self, deviceid):

        sql = "SELECT * FROM RelationDeviceToOrg WHERE DeviceID = " + str(deviceid)
        orgid = self.ms.ExecQuery(sql)[0]['OrgID']
        return orgid
    #根据设备id查询组织类型
    def deviceID2orgType(self, deviceid):
        sql = "SELECT * FROM RelationDeviceToOrg WHERE DeviceID = " + str(deviceid)
        orgid = self.ms.ExecQuery(sql)[0]['OrgID']
        sql1 = "SELECT * FROM Orgnization WHERE OrgID = " + str(orgid)
        orgtype = self.ms.ExecQuery(sql1)[0]['OrgType']
        return orgtype
    #根据设备id查询设备类型
    def deviceID2deviceType(self, deviceid):
        sql = "SELECT * FROM Device WHERE ID = " + deviceid
        deviceType = self.ms.ExecQuery(sql)[0]['DeviceType']
        return deviceType
    #根据设备类型查询位置
    def deviceID2position(self, deviceid):
        sql = "SELECT * FROM Device WHERE ID = " + deviceid
        position = self.ms.ExecQuery(sql)[0]['Position']
        return position

    #数据库创建新package
    def createPackage(self, orgID, PackageLevel, IsDeal, IsFinish):
        sql = "INSERT INTO AlarmPackage (OrgID, PackageLevel,IsDeal, IsFinish) VALUES ( " + str(orgID) + "," + str(PackageLevel) + "," +str(IsDeal) + "," + str(IsFinish)+")"
        id = self.ms.executeAndGetId(sql)
        return id

    def updatePackageLevel(self, packageId, level):
        sql = "UPDATE AlarmPackage SET PackageLevel =" + str(level) + "WHERE ID = " + str(packageId)
        self.ms.ExecNonQuery(sql)

    def updateAlarmEvent(self, packageId, Id):
        sql = "UPDATE AlarmEvent SET PackageID =" + str(packageId) + "WHERE ID = " + str(Id)
        self.ms.ExecNonQuery(sql)

    #def updatePackageFinishInfo(self, packageId):
     #   sql = "UPDATE AlarmPackage SET IsFinish =" + str(1) +", FinishReason = " + "'Finished: Program'" + " WHERE ID = " + str(packageId)
     #   self.ms.ExecNonQuery(sql)

    def updatePackageFinishInfo(self, packageId, userName, time, record):
        if userName == None:
            sql = "UPDATE AlarmPackage SET IsFinish =" + str(1) + ", FinishReason = " + "'Finished : Program'"\
                  + "WHERE ID = " + str(packageId)
        else:
            sql = "UPDATE AlarmPackage SET IsFinish =" + str(1) + ", FinishReason = " + "'Finished : User'" \
                  + ", IsDeal = " + str(1) + ", ProcUserName = " + "'" + str(
                userName) + "'" + ", ProcTime = " + "'" + str(time) + "'" \
                  + ", ProcRecord = " + "'" + str(record) + "'" + "WHERE ID = " + str(packageId)
        self.ms.ExecNonQuery(sql)

    def selectOrgIdByPackageId(self, packageId):
        sql = "SELECT * FROM AlarmPackage WHERE ID = " + str(packageId)
        orgid = self.ms.ExecQuery(sql)[0]['OrgID']
        return orgid

    def selectAlarmEventByPackageId(self, packageId):
        sql = "SELECT * FROM AlarmEvent WHERE PackageID = " + str(packageId)
        eventList = self.ms.ExecQuery(sql)
        return eventList

    def selectOrgTypeByOrgId(self,orgId):
        sql = "SELECT * FROM Orgnization WHERE OrgID = " + str(orgId)
        orgType = self.ms.ExecQuery(sql)[0]['OrgType']
        return orgType

    def selectDeviceId(self,deviceId):
        sql = "SELECT * FROM Device WHERE ID = " + str(deviceId)
        deviceId = self.ms.ExecQuery(sql)[0]['ID']
        return deviceId

    def updateDeviceRegisterInfo(self, deviceId, isRegistered):
        sql = "UPDATE Device SET IsRegistered =" + str(isRegistered) + "WHERE ID = " + str(deviceId)
        self.ms.ExecNonQuery(sql)

    def insertChannelRegisterInfo(self, channelname, channelno, channeltype, channelip,inputdeviceid, channelport):
        sql = "INSERT INTO Channel(ChannelName, ChannelNumber, ChannelType, ChannelHostIP, InputDeviceID, ChannelHostPort) VALUES (" \
              + "'" +str(channelname) + "'" + "," + str(channelno) + "," + str(channeltype) + "," + "'" +str(channelip) + "'" + "," + str(inputdeviceid) + "," +\
            str(channelport) + ")"
        self.ms.ExecNonQuery(sql)

    def delChannelRegisterInfo(self, deviceId):
        sql = "DELETE FROM Channel WHERE InputDeviceID = " + str(deviceId)
        self.ms.ExecNonQuery(sql)

    def selectDictInfo(self, tableName):
        sql = "SELECT * FROM " + str(tableName)
        rows = self.ms.ExecQuery(sql)
        return rows

    def moveEvent2Record(self, id, procUserName, procTime, procRecord):
        selectsql = "SELECT DeviceID, ChannelID, AlarmTime, AlarmType, Score, PictrueUrl, \
            Status, ProcedureData, AlarmLevel, PackageID FROM AlarmEvent where ID=" + str(id)

        resList = self.ms.ExecQuery(selectsql)[0]
        orgId = self.selectOrgIdByPackageId(resList['PackageID'])
        insertsql = "INSERT INTO AlarmEventRecord (OrgID, DeviceID, AlarmTime, AlarmType, ChannelID, Score, PictrueUrl, ProcUserName," \
                    "ProcTime, ProcRecord, ProcedureData,AlarmLevel, PackageID) VALUES (" + str(orgId) + "," + str(
            resList["DeviceID"]) + "," + "'" + str(resList["AlarmTime"]) + "'" + "," + str(resList["AlarmType"]) \
                    + "," + str(resList["ChannelID"]) + "," + str(resList["Score"]) + "," + "'" + str(
            resList["PictrueUrl"]) + "'" \
                    + "," + "'" + str(procUserName) + "'" + "," + "'" + str(procTime) + "'" + "," + "'" + str(
            procRecord) + "'" + "," + "'" + str(resList["ProcedureData"]) + "'" + "," + str(resList["AlarmLevel"]) + "," \
                    + str(resList["PackageID"]) + ")"
        deletesql = "DELETE FROM AlarmEvent where ID=" + str(id)

        self.ms.ExecMove(id, insertsql, deletesql)
if __name__ == '__main__':
    sqlcluster = SQLCluster()
    sqlcluster.delChannelRegisterInfo(1)
    sqlcluster.insertChannelRegisterInfo('原理样机通道3', 3, 3000, '10.25.12.1', 1, 9000)
    #print sqlcluster.deviceID2orgID(str(1))
    #print sqlcluster.deviceID2deviceType(str(1))
    #print sqlcluster.deviceID2orgType(str(1))
    #print sqlcluster.deviceID2position(str(1))
    #print sqlcluster.updateDeviceRegisterInfo(1,1)
    #id = sqlcluster.createPackage(16,1,1,0)
    #print id
    #sqlcluster.updatePackage(3, 4)
    #sqlcluster.updateAlarmEvent(1, 208)
    #sqlcluster.updatePackageFinishInfo(7)
    #sqlcluster.updatePackageFinishInfoByUser(8, 'liuqiang', '2017-02-28 14:07:17.000', '核实通过')
    #print sqlcluster.selectOrgIdByPackageId(5)
