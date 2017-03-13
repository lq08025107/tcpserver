# -*- coding=utf-8 -*-
import pymssql

from DBUtils.PooledDB import PooledDB
import ConfigParser
from LogModule import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)
class MSSQL(object):
    __pool = None
    def __init__(self, choice = 'd'):
        if choice == 'd':
            self._conn = MSSQL.__getConn()
            self._cursor = self._conn.cursor()
        else:
            MSSQL.__pool = None
            self._conn = MSSQL.getConn()
            self._cursor = self._conn.cursor()

    @staticmethod
    def __getConn():
        cp = ConfigParser.SafeConfigParser()
        cp.read('config\config.ini')
        if MSSQL.__pool is None:
            __pool = PooledDB(creator=pymssql, mincached=1, maxcached=5,
                              host=cp.get('db', 'ms_host'), user=cp.get('db', 'ms_user'), password=cp.get('db', 'ms_passwd'),
                              database=cp.get('db', 'ms_db'), charset=cp.get('db', 'ms_dbcharset'), as_dict=True)
            return __pool.connection()

    @staticmethod
    def getConn():
        cp = ConfigParser.SafeConfigParser()
        cp.read('config\config.ini')
        if MSSQL.__pool is None:
            __pool = PooledDB(creator=pymssql, mincached=1, maxcached=5,
                              host=cp.get('db', 'ms_host'), user=cp.get('db', 'ms_user'), password=cp.get('db', 'ms_passwd'),
                              database=cp.get('db', 'ms_db'), charset=cp.get('db', 'ms_dbcharset'))
            return __pool.connection()
    def dispose(self, isEnd = 1):
        self._cursor.close()
        self._conn.close()


    def ExecQuery(self, sql):

        self._cursor.execute(sql)
        resList = self._cursor.fetchall()
        #self.dispose()
        return resList

    def ExecNonQuery(self, sql):
        #if self._cursor._closed is True:
        #    self.__init__()
        self._cursor.execute(sql)
        self._conn.commit()
        #self.dispose()

    #liuqiang add for purpose of getting id
    def executeAndGetId(self, sql, param=None):

        if param == None:
            self._cursor.execute(sql)
        else:
            self._cursor.execute(sql, param)
        id = self._cursor.lastrowid
        self._conn.commit()
        #self.dispose()
        return id

    def ExecMove(self, id, insertsql, deletesql):

        try:
            self._cursor.execute(insertsql)
            self._cursor.execute(deletesql)
            self._conn.commit()
        except Exception, e:
            logger.error(e)
            self._conn.rollback()
        #self.dispose()



def main():
    # ms = MSSQL(host="10.25.18.9",user="sa",pwd="p@ssw0rd",db="IVAS")
    #ms = MSSQL()

    # ms.ExecNonQuery("Delete FROM AlarmEvent where ID=" + str(30))
    # ms.ExecNonQuery("Insert INTO AlarmEventRecord "
    #                 "(OrgID, DeviceID, AlarmTime, AlarmType, ChannelID, Score, PictrueUrl, ProcUserName, "
    #                 "ProcTime, ProcRecord, ProcedureData) VALUES "
    #                 "(10, 4, '2017-02-23 15:54:00.000', 300, 4, 59.8, '11111', 'ZC', '2017-02-23 15:54:00.000', 'Hello', '1')")

    # test1 = "Insert INTO AlarmEventRecord " \
    #         "(OrgID, DeviceID, AlarmTime, AlarmType, ChannelID, Score, PictrueUrl, ProcUserName," \
    #         "ProcTime, ProcRecord, ProcedureData) VALUES " + str(("10", DeviceID, str(AlarmTime.strftime("%Y-%m-%d %H:%M:%S.000")), AlarmType, ChannelID, Score, str(PictrueUrl), 'ZC', '2017-02-23 15:54:00.000', "ZD DO", str(ProcedureData)))
    # print test1
    # ms.ExecNonQuery(test1)
    ms.dispose()


if __name__ =='__main__':
    main()
    #event2record(19, 'liuqiang',  '2017-02-24 14:37:15.000','处理完毕')