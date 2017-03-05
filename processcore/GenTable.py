# coding=utf-8
import Log
import ConfigParser
import MysqlCon
import sys
import json
from LogModule import setup_logging

import logging
setup_logging()
logger = logging.getLogger(__name__)
# 配置utf-8输出环境
reload(sys)
sys.setdefaultencoding('utf-8')

class MenTable:

    def __init__(self):

        cp = ConfigParser.SafeConfigParser()
        cp.read('processcore\db.ini')
        cols_cnt = cp.get('table', 'cols_cnt')
        relation_table_name = cp.get('table', 'relation_table_name')
        cols_table_name = cp.get('table', 'cols_table_name')
        alarm_level_table = cp.get('table', 'alarm_level_table');
        tables = cols_table_name.split(',')
        logger.info("tables %s" % tables)
        logger.info('relation_table_name: %s' % relation_table_name)
        logger.info('table cnt: %s' % cols_cnt)
        logger.info('alarm_level_table: %s' % alarm_level_table)

        conn = MysqlCon.MySqlUtil()
        item = conn.getTableNames(tables)
        logger.info('item: %s' % item)

        self.arr = self.getList(item, 0)
        logger.info('arr: %s' % self.arr)
        results = conn.fetchRows(relation_table_name)
        logger.info('result: %s' % results)

        levels = conn.fetchRows(alarm_level_table)

        for i in results:
            self.arr[i[1] - 1][i[2] - 1][i[4] - 1][i[5] - 1][i[6] - 1] = levels[i[9] - 1][3]
        logger.info('arr: %s' % json.dumps(self.arr, encoding='UTF-8', ensure_ascii=False))

    def getList(self, arr, index):
        if index == len(arr) - 1:
            return [0] * arr[index]
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
    menTable.query([1, 3])
    queryList = [1, 2, 2, 2, 4]
    level = menTable.query(queryList)
    logger = Log.Logger.getInstance()
    logger.info('level: %s', level)