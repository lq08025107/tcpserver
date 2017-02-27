import Queue
import random
from LogicCoreModule import EventProcessThread
from LogicCoreModule import NoticeProcessThread

class GlobalParams(object):
    EventInitCount = 3
    NoticeInitCount = 2
    EventProcessThreads = []
    NoticeProcessThreads = []

    ClientOnlineList = {}
    ClientOnlineLock = False

def initProcessThread():
    print "Initlizing Process Thread ...."
    for i in range(0, GlobalParams.EventInitCount):
        eventProcessThread = EventProcessThread()
        GlobalParams.EventProcessThreads.append(eventProcessThread)
        eventProcessThread.start()

    for i in range(0, GlobalParams.NoticeInitCount):
        noticeProcessThread = NoticeProcessThread()
        GlobalParams.NoticeProcessThreads.append(noticeProcessThread)
        noticeProcessThread.start()
    print "InitlizeProcess Thread finish"


def addEventProcessThread():
    eventProcessThread = EventProcessThread()
    GlobalParams.EventProcessThreads.append(eventProcessThread)
    eventProcessThread.start()

def addNoticeProcessThread():
    noticeProcessThread = NoticeProcessThread()
    GlobalParams.NoticeProcessThreads.append(noticeProcessThread)
    noticeProcessThread.start()

def getEventProcessThread():
    i = random.randint(0, len(GlobalParams.EventProcessThreads) - 1)
    return GlobalParams.EventProcessThreads[i].ProcessQueue

def getNoticeProcessThread():
    i = random.randint(0, len(GlobalParams.NoticeProcessThreads) - 1)
    return GlobalParams.NoticeProcessThreads[i].NoticeQueue


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
    print ClientIP

def DelOneClient(ClientIP):
    GlobalParams.ClientOnlineLock = True

    if GlobalParams.ClientOnlineList[ClientIP] != None:
        GlobalParams.ClientOnlineList[ClientIP].connectionLost
    GlobalParams.ClientOnlineLock = False