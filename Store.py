from MsgParserBox import MsgParser
from utiltool.DBOperator import MSSQL
import GlobalParams
from threading import Thread
import Queue
from LogModule import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)

class StoreProcessThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.StoreQueue = Queue.Queue()
        self.IsRunning = True

    def StopThread(self):
        self.IsRunning = False

    def run(self):
        logger.info("Store " + self.getName() + " Start Running")

        while self.IsRunning:
            while self.StoreQueue.not_empty:
                ms = MSSQL()
                message = self.StoreQueue.get()
                parser = MsgParser()
                try:
                    dataList = parser.parse(message)
                    # save as db
                    insertsql = parser.constr(dataList)
                    id = ms.executeAndGetId(insertsql)
                    logger.info("Message has been inserted into db successfully, id: " + str(id))

                    # send to application module
                    notice_queue = GlobalParams.getNoticeProcessQueue()
                    notice_queue.put(id)

                except Exception, e:
                    # log as file
                    logger.error("Error occured!!!", exc_info=True)
        logger.info("Store " + self.getName() + " Stop Run")



