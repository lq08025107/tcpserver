import Queue
import random
from LogicCoreModule import EventProcessThread
from LogicCoreModule import NoticeProcessThread
from LogicCoreModule import PCProcessThread
from Store import StoreProcessThread
from processcore.GenTable import MenTable
from FTPServer import FTPServerThread
from processcore.AutoSco import AutoScore
from Reactor import TwistedProcessThread
from LogModule import setup_logging


import logging

setup_logging()
logger = logging.getLogger(__name__)

class GlobalParams(object):
    EventInitCount = 1
    NoticeInitCount = 1
    StoreInitCount = 1
    PCInitCount = 1

    EventProcessThreads = []
    NoticeProcessThreads = []
    StoreProcessThreads = []
    PCProcessThreads = []

    ClientOnlineList = {}
    ClientOnlineLock = False

    autoSco = AutoScore()
    genTable = MenTable()

def initProcessThread():
    logger.info("Start Initlizing Process Thread.")

    twistedProcessThread = TwistedProcessThread()
    twistedProcessThread.start()

    #ftpServerThread = FTPServerThread()
    #ftpServerThread.start()

    for i in range(0, GlobalParams.EventInitCount):
        eventProcessThread = EventProcessThread()
        GlobalParams.EventProcessThreads.append(eventProcessThread)
        eventProcessThread.start()

    for i in range(0, GlobalParams.NoticeInitCount):
        noticeProcessThread = NoticeProcessThread()
        GlobalParams.NoticeProcessThreads.append(noticeProcessThread)
        noticeProcessThread.start()

    for i in range(0, GlobalParams.StoreInitCount):
        storeProcessThread = StoreProcessThread()
        GlobalParams.StoreProcessThreads.append(storeProcessThread)
        storeProcessThread.start()

    for i in range(0, GlobalParams.PCInitCount):
        pcProcessThread = PCProcessThread()
        GlobalParams.PCProcessThreads.append(pcProcessThread)
        pcProcessThread.start()



    logger.info("Finish Initlizing Process Thread.")


def addEventProcessThread():
    eventProcessThread = EventProcessThread()
    GlobalParams.EventProcessThreads.append(eventProcessThread)
    eventProcessThread.start()

def addNoticeProcessThread():
    noticeProcessThread = NoticeProcessThread()
    GlobalParams.NoticeProcessThreads.append(noticeProcessThread)
    noticeProcessThread.start()

def addStoreProcessThread():
    storeProcessThread = StoreProcessThread()
    GlobalParams.StoreProcessThreads.append(storeProcessThread)
    storeProcessThread.start()

def getEventProcessQueue():
    i = random.randint(0, len(GlobalParams.EventProcessThreads) - 1)
    return GlobalParams.EventProcessThreads[i].ProcessQueue

def getNoticeProcessQueue():
    i = random.randint(0, len(GlobalParams.NoticeProcessThreads) - 1)
    return GlobalParams.NoticeProcessThreads[i].NoticeQueue

def getStoreProcessQueue():
    i = random.randint(0, len(GlobalParams.StoreProcessThreads) - 1)
    return GlobalParams.StoreProcessThreads[i].StoreQueue

def GetAutoScoreInstance():
    return GlobalParams.autoSco

def GetGenTable():
    return GlobalParams.genTable



def GetOneClient(ClientIP):
    return GlobalParams.ClientOnlineList[ClientIP]

def GetAllClient():
    return GlobalParams.ClientOnlineList

def AddOneClient(Client, ClientIP):
    GlobalParams.ClientOnlineLock = True

    if not GlobalParams.ClientOnlineList.has_key(ClientIP):
        GlobalParams.ClientOnlineList[ClientIP] = Client
    else:
        GlobalParams.ClientOnlineList[ClientIP].connectionLost
        GlobalParams.ClientOnlineList[ClientIP] = Client

        GlobalParams.ClientOnlineLock = False


def DelOneClient(ClientIP):
    GlobalParams.ClientOnlineLock = True

    if GlobalParams.ClientOnlineList[ClientIP] != None:
        GlobalParams.ClientOnlineList[ClientIP].connectionLost
    GlobalParams.ClientOnlineLock = False