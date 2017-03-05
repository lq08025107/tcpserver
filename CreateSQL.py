# -*- coding=utf-8 -*-
from LogModule import setup_logging
from utiltool.DBOperator import MSSQL

import logging

class SQLCluster():
    #根据设备id查询组织id
    def deviceID2orgID(self, deviceid):
        ms = MSSQL()
        sql = "SELECT * FROM RelationDeviceToOrg WHERE DeviceID = " + str(deviceid)
        orgid = ms.ExecQuery(sql)[0]['OrgID']
        return orgid
    #根据设备id查询组织类型
    def deviceID2orgType(self, deviceid):
        ms = MSSQL()
        sql = "SELECT * FROM RelationDeviceToOrg WHERE DeviceID = " + str(deviceid)
        orgid = ms.ExecQuery(sql)[0]['OrgID']
        sql1 = "SELECT * FROM Orgnization WHERE OrgID = " + str(orgid)
        orgtype = ms.ExecQuery(sql1)[0]['OrgType']
        return orgtype
    #根据设备id查询设备类型
    def deviceID2deviceType(self, deviceid):
        ms = MSSQL()
        sql = "SELECT * FROM Device WHERE ID = " + deviceid
        deviceType = ms.ExecQuery(sql)[0]['DeviceType']
        return deviceType
    #根据设备类型查询位置
    def deviceID2position(self, deviceid):
        ms = MSSQL()
        sql = "SELECT * FROM Device WHERE ID = " + deviceid
        position = ms.ExecQuery(sql)[0]['Position']
        return position

    #数据库创建新package
    def createPackage(self, orgID, PackageLevel, IsDeal, IsFinish):
        ms = MSSQL()
        sql = "INSERT INTO AlarmPackage (OrgID, PackageLevel,IsDeal, IsFinish) VALUES ( " + str(orgID) + "," + str(PackageLevel) + "," +str(IsDeal) + "," + str(IsFinish)+")"
        print sql
        id = ms.executeAndGetId(sql)
        return id

    def updatePackageLevel(self, packageId, level):
        ms = MSSQL()
        sql = "UPDATE AlarmPackage SET PackageLevel =" + str(level) + "WHERE ID = " + str(packageId)
        ms.ExecNonQuery(sql)

    def updateAlarmEvent(self, packageId, Id):
        ms = MSSQL()
        sql = "UPDATE AlarmEvent SET PackageID =" + str(packageId) + "WHERE ID = " + str(Id)
        ms.ExecNonQuery(sql)

    def updatePackageFinishInfo(self, packageId):
        ms = MSSQL()
        sql = "UPDATE AlarmPackage SET IsFinish =" + str(1) +", FinishReason = " + "'Finished: Program'" + " WHERE ID = " + str(packageId)
        ms.ExecNonQuery(sql)

    def updatePackageFinishInfoByUser(self, packageId, userName, time, record):
        ms = MSSQL()
        sql = "UPDATE AlarmPackage SET IsFinish =" + str(1) + ", FinishReason = " + "'Finished : User'"\
              + ", IsDeal = " + str(1) + ", ProcUserName = " + "'"+ str(userName) + "'"+", ProcTime = " + "'"+str(time) +"'"\
              + ", ProcRecord = " + "'"+str(record) + "'" + "WHERE ID = " + str(packageId)
        print sql
        ms.ExecNonQuery(sql)

    def selectOrgIdByPackageId(self, packageId):
        ms = MSSQL()
        sql = "SELECT * FROM AlarmPackage WHERE ID = " + str(packageId)
        orgid = ms.ExecQuery(sql)[0]['OrgID']
        return orgid

    def selectAlarmEventByPackageId(self, packageId):
        ms = MSSQL()
        sql = "SELECT * FROM AlarmEvent WHERE PackageID = " + str(packageId)
        eventList = ms.ExecQuery(sql)
        return eventList
if __name__ == '__main__':
    sqlcluster = SQLCluster()
    print sqlcluster.deviceID2orgID(str(1))
    print sqlcluster.deviceID2deviceType(str(1))
    print sqlcluster.deviceID2orgType(str(1))
    print sqlcluster.deviceID2position(str(1))
    #id = sqlcluster.createPackage(16,1,1,0)
    #print id
    #sqlcluster.updatePackage(3, 4)
    #sqlcluster.updateAlarmEvent(1, 208)
    #sqlcluster.updatePackageFinishInfo(7)
    #sqlcluster.updatePackageFinishInfoByUser(8, 'liuqiang', '2017-02-28 14:07:17.000', '核实通过')
    #print sqlcluster.selectOrgIdByPackageId(5)
    for event in sqlcluster.selectAlarmEventByPackageId(9):
        print event