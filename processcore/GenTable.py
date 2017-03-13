# coding=utf-8
import ConfigParser
from CreateSQL import SQLCluster
import sys
import json
import utiltool.DBOperator
from LogModule import setup_logging

import logging
setup_logging()
logger = logging.getLogger(__name__)
# 配置utf-8输出环境
reload(sys)
sys.setdefaultencoding('utf-8')


class MenTable:

    def __init__(self):
        self.sqlcluster = SQLCluster('astuple')
        cp = ConfigParser.SafeConfigParser()
        cp.read('config\config.ini')
        cols_cnt = cp.get('table', 'cols_cnt')
        relation_table_name = cp.get('table', 'relation_table_name')
        cols_table_name = cp.get('table', 'cols_table_name')
        alarm_level_table = cp.get('table', 'alarm_level_table')
        tables = cols_table_name.split(',')
        logger.debug("tables %s" % tables)
        logger.debug('relation_table_name: %s' % relation_table_name)
        logger.debug('table cnt: %s' % cols_cnt)
        logger.debug('alarm_level_table: %s' % alarm_level_table)


        item = self.getTableNames(tables)
        logger.debug('item: %s' % item)

        self.arr = self.getList(item, 0)
        logger.debug('arr: %s' % self.arr)
        results = self.fetchRows(relation_table_name)
        logger.debug('result: %s' % results)

        levels = self.fetchRows(alarm_level_table)

        for i in results:
            #self.arr[i[1] - 1][i[2] - 1][i[4] - 1][i[5] - 1][i[6] - 1] = levels[i[9] - 1][0]
            self.arr[i[1] - 1][i[2] - 1][i[4] - 1][i[5] - 1][i[6] - 1] = i[9]
        logger.debug('arr: %s' % json.dumps(self.arr, encoding='UTF-8', ensure_ascii=False))

    def getTableNames(self, tables):
        item = []
        for tableName in tables:
            rows = self.sqlcluster.selectDictInfo(tableName)
            rowCount = len(rows)
            item.append(rowCount)
        return item

    def fetchRows(self, relation_table_name):
        rows = self.sqlcluster.selectDictInfo(relation_table_name)
        return rows

    def getList(self, arr, index):
        if index == len(arr) - 1:
            return [1] * arr[index]
        else:
            cur_list = []
            for i in range(arr[index]):
                cur_list.append(self.getList(arr, index + 1))
            return cur_list

    def query(self, i):
        if type(i) == list and len(i) == 5:
            return self.arr[i[0] - 1][i[1] - 1][i[2] - 1][i[3] - 1][i[4] - 1]
        return -1



if __name__ == '__main__':
    menTable = MenTable()
    info = menTable.fetchRows('RulesTable')
    print info
    # menTable.query([1, 3])
    # queryList = [1, 2, 2, 2, 4]
    # level = menTable.query(queryList)
    # logger = Log.Logger.getInstance()
    # logger.info('level: %s', level)

    # mysqlUtil = MySqlUtil()
    # insertRelationShipSql = "select * from AlarmEvent"
    # conn = mysqlUtil.getConn()
    # cur = conn.cursor()
    # for i in range(1, 6):
    #     for j in range(1, 4):
    #         for k in range(1, 6):
    #             for m in range(1, 4):
    #                 for n in range(1, 5):
    #                     value = random.randint(1, 5)
    #                     sql = "insert into RulesTable(OrgType,Position,AlarmType,DeviceType,DateAttribute,TimeAttribute,AlarmLevel) values(%d, %d, %d, 1,%d, %d, %d)" \
    #                           % (i, j, k, m, n, value)
    #                     try:
    #                         cur.execute(sql)
    #                         conn.commit()
    #                     except:
    #                         conn.rollback()
    #                         Logger.getInstance().info(traceback.format_exc())