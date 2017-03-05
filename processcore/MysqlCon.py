# coding=utf-8
import MySQLdb
from Log import Logger
import traceback
import ConfigParser
import pymssql
import random
from LogModule import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)
class MySqlUtil:
    def __init__(self, host='localhost', port=3306, user='root', passwd='asd123', db='wbqzgl', unix_socket='/tmp/mysql.sock'):
        cp = ConfigParser.SafeConfigParser()
        cp.read('processcore\db.ini')
        type = cp.get('db', 'db_type')
        host, user, passwd, db_name = '', '', '', ''
        self.logger = logger
        if type == 'mysql':
            host = cp.get('db', 'my_host')
            user = cp.get('db', 'my_user')
            passwd = cp.get('db', 'my_passwd')
            db = cp.get('db', 'my_db')
            unix_socket = cp.get('db', 'my_unix_socket')
            self.logger.info('host: %s, user: %s, passwd: %s, db: %s, socket: %s'
                            % (host, user, passwd, db, unix_socket))
            self.conn = MySQLdb.connect(host=host, port=port, user=user, passwd=passwd, db=db,
                                        unix_socket=unix_socket)
            self.logger.info('connect to %s' % type)
        elif type == 'mssql':
            host = cp.get('db', 'ms_host')
            user = cp.get('db', 'ms_user')
            passwd = cp.get('db', 'ms_passwd')
            db = cp.get('db', 'ms_db')
            self.logger.info('host: %s, user: %s, passwd: %s, db: %s' % (host, user, passwd, db))
            self.conn = pymssql.connect(host = host, user = user, password = passwd, database = db, charset="utf8")
            self.logger.info('connect to %s' % type)

    def getCur(self):
        if not self.conn:
            raise(NameError, 'no database connect')
        cur = self.conn.cursor()
        if not cur:
            raise(NameError, 'connect error')
        else:
            return cur

    def getConn(self):
        return self.conn

    def getTableNames(self, tables):
        item = []
        for tableName in tables:
            cursor = self.conn.cursor()
            cursor.execute("select count(*) from " + tableName)
            rowCount = cursor.fetchone()
            item.append(rowCount[0])
        return item

    def fetchRows(self, relation_table_name):
        cursor = self.conn.cursor()
        cursor.execute('select * from ' + relation_table_name)
        return cursor.fetchall()

if __name__ == '__main__':
    mysqlUtil = MySqlUtil()
    insertRelationShipSql = "select * from AlarmEvent"
    conn = mysqlUtil.getConn()
    cur = conn.cursor()
    for i in range(1, 6):
        for j in range(1, 4):
            for k in range(1, 6):
                for m in range(1, 4):
                    for n in range(1, 5):
                        value = random.randint(1, 5)
                        sql = "insert into RulesTable(OrgType,Position,AlarmType,DeviceType,DateAttribute,TimeAttribute,AlarmLevel) values(%d, %d, %d, 1,%d, %d, %d)" \
                              % (i, j, k, m, n, value)
                        try:
                            cur.execute(sql)
                            conn.commit()
                        except:
                            conn.rollback()
                            Logger.getInstance().info(traceback.format_exc())




