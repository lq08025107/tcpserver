# coding=utf-8
import Log
import ConfigParser
import MysqlCon
import sys
import Queue
import json
import threading
import time
import threadpool
import AlarmUtil
from LogModule import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)
# 配置utf-8输出环境
reload(sys)
sys.setdefaultencoding('utf-8')

class Node:
    def __init__(self, id=0, data={'kind': 'aa', 'level': 1, 'position': ''}, children=None):
        self.id = id
        self.data = data
        self.children = children

    def setChildren(self, children={}):
        self.children = children

class AlarmNode:
    def __init__(self, id=0, org=0, req_que_size=100, resp_que_size=100, threadpo=None,
                 alarmDura={}, accu_threshold=0, max_alarm_level=5, parentRespQueue=None):
        self.id = id
        self.org = org
        self.req_que_size = req_que_size
        self.resp_que_size = resp_que_size
        self.threadpo = threadpo
        self.alarmDura = alarmDura
        self.alarmList = []
        self.alarmScoreMap = {}
        self.preTime = 0
        self.duration = 0
        self.accu_threshold = accu_threshold
        self.reqQueue = Queue.Queue(maxsize=self.req_que_size)
        self.respQueue = Queue.Queue(maxsize=self.resp_que_size)
        self.max_alarm_level = max_alarm_level
        self.parentRespQueue = parentRespQueue
        self.logger = Log.Logger.getInstance()
        self.isStop= True
        self.threads = threadpool.makeRequests(self.alaMsg, [(None, None)])
        self.lock = threading.Lock()
        self.currentAlarmLevel = {'level': 0, 'alarmId': 0}
        self.maxAlarmId = 0

        #get a AlarmUtil
        self.alarmUtil = AlarmUtil.AlarmUtil()


    def endPackage(self, reason):
        self.alarmList = []
        self.alarmScoreMap = {}
        self.preTime = 0
        self.duration = 0
        self.currentAlarmLevel = {'level': 0, 'alarmId': 0}
        self.maxAlarmId = 0
        self.parentRespQueue.put({'packageId': 0, 'reason': reason})

    def start(self):
        self.threadpo.putRequest(self.threads[0])

    def alaMsg(self):
        logger.debug('org %s, begin a new package!' % (self.org))
        #开启一个新包的线程
        self.packageId = self.alarmUtil.createPackage(self.org, 1, False)
        while True:
            try:
                msg = self.reqQueue.get(True, 1)
            except:
                if self.isStop:
                    logger.debug('org %d end package for timeout' % (self.org))
                    self.endPackage('timeout')
                    break
                else:
                    continue
            if 'stop' in msg:
                logger.debug('org %d end package by user' % (self.org))
                self.endPackage('user')
                self.isStop = True
                break
            alarmId = msg['alarmId']
            deviceId = msg['deviceId']
            level = msg['currentAlarmLevel']
            logger.debug('get msg: %s, duration: %s, current list: %s, current map: %s, level: %s'
                              % (msg, self.duration, self.alarmList, self.alarmScoreMap, self.currentAlarmLevel))

            self.alarmList.append(alarmId)
            if (not (alarmId in self.alarmScoreMap)):
                self.alarmScoreMap.setdefault(alarmId, {'num': 1, 'level': level})
            else:
                self.alarmScoreMap[alarmId]['num'] += 1
                newLevel = (int)(self.alarmScoreMap[alarmId]['num'] / self.accu_threshold) + level
                if(newLevel < self.max_alarm_level and newLevel > self.alarmScoreMap[alarmId]['level']):
                    self.alarmScoreMap[alarmId]['level'] = newLevel
                elif newLevel >= self.max_alarm_level:
                    self.alarmScoreMap[alarmId]['level'] = self.max_alarm_level
            if self.currentAlarmLevel['level'] < self.alarmScoreMap[alarmId]['level']:
                self.currentAlarmLevel['level'] = self.alarmScoreMap[alarmId]['level']
                self.currentAlarmLevel['alarmId'] = alarmId

            self.preTime = time.time()
            self.duration = self.alarmDura[alarmId]
            logger.debug('get msg: %s, duration: %s, current list: %s, current map: %s, level: %s'
                              % (msg, self.duration, self.alarmList, self.alarmScoreMap, self.currentAlarmLevel))
            #更新包
            self.alarmUtil.updatePackageInfo(self.packageId, msg['id'], self.currentAlarmLevel['level'])

class MockCmd:
    reqQue = None
    respQue = None

    @staticmethod
    def sendMsg(msg):
        MockCmd.reqQue.put(msg)

class AutoScore:

    count = 1
    def __init__(self):
        self.logger = Log.Logger.getInstance()
        cp = ConfigParser.SafeConfigParser()
        cp.read('processcore\db.ini')
        self.req_que_size = (int)(cp.get('autoLevel', 'req_que_size'))
        self.resp_que_size = (int)(cp.get('autoLevel', 'resp_que_size'))
        self.threadpoolSize = (int)(cp.get('autoLevel', 'threadpoolSize'))
        self.accu_threshold = (int)(cp.get('autoLevel', 'accu_threshold'))
        self.max_alarm_level = (int)(cp.get('autoLevel', 'max_alarm_level'))
        self.threadpo = threadpool.ThreadPool(self.threadpoolSize)
        self.root = Node()
        self.reqQueue = Queue.Queue(maxsize=self.req_que_size)
        self.respQueue = Queue.Queue(maxsize=self.resp_que_size)
        self.alarmDura = {}
        children = {}
        for i in cp.get('autoLevel', 'alarm').split(','):
            key = (int)(i.split('-')[0])
            value = (int)(i.split('-')[1])
            self.alarmDura[key] = value
        for key in cp.get('autoLevel', 'org').split(','):
            children[(int)(key)] = AlarmNode(org=(int)(key), req_que_size=self.req_que_size,
                                             resp_que_size=self.resp_que_size, threadpo=self.threadpo,
                                             alarmDura=self.alarmDura, accu_threshold=self.accu_threshold,
                                             max_alarm_level=self.max_alarm_level, parentRespQueue=self.respQueue)
        logger.info('init: %s, %s' % (self.alarmDura, children))
        self.root.setChildren(children)
        self.alaMsgTask = threadpool.makeRequests(self.alaMsg, [(None, None)])
        self.scanTimeTask = threadpool.makeRequests(self.scanTime, [(None, None)])
        self.threadpo.putRequest(self.alaMsgTask[0])
        self.threadpo.putRequest(self.scanTimeTask[0])

    def alaMsg(self):
        while True:
            msg = self.reqQueue.get()
            org = (int)(msg['orgId'])
            self.root.children[org].reqQueue.put(msg)

    def scanTime(self):
        while True:
            for i in self.root.children:
                leftSeconds = self.root.children[i].duration - (time.time() - self.root.children[i].preTime);
                #if leftSeconds >= 0:
                    #self.logger.debug('org %d close to %ds' % (self.root.children[i].org, leftSeconds))
                if (leftSeconds < 0):
                    self.root.children[i].isStop = True
                if (not self.root.children[i].reqQueue.empty()) and self.root.children[i].isStop:
                    self.root.children[i].isStop = False
                    self.root.children[i].start()
            time.sleep(1)

if __name__ == '__main__':
    msg = {'orgId': 1, 'deviceId': 2, 'alarmId': 3, 'dateArrId': 4, 'timeArrId': 5, 'currentAlarmLevel': 0}
    node = Node()
    autoScore = AutoScore()

    while True:
        msg = input('')
        autoScore.reqQueue.put(msg)
#autoScore.respQueue.get()
# {'orgId': 1, 'deviceId': 2, 'alarmId': 3, 'dateArrId': 4, 'timeArrId': 5, 'currentAlarmLevel': 2, 'id': 1}
# {'orgId': 1, 'deviceId': 2, 'alarmId': 2, 'dateArrId': 4, 'timeArrId': 5, 'currentAlarmLevel': 2}
# {'orgId': 1, 'deviceId': 2, 'alarmId': 1, 'dateArrId': 4, 'timeArrId': 5, 'currentAlarmLevel': 2}
# {'orgId': 2, 'deviceId': 2, 'alarmId': 3, 'dateArrId': 4, 'timeArrId': 5, 'currentAlarmLevel': 2}
# {'orgId': 3, 'deviceId': 2, 'alarmId': 3, 'dateArrId': 4, 'timeArrId': 5, 'currentAlarmLevel': 2}
# {'orgId': 1, 'stop': 1}