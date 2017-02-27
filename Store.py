from MyQueue import queue
from MsgParserBox import MsgParser
from utiltool.DBOperator import MSSQL
import GlobalParams
from LogModule import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)


def start_store():
    while(True):

        if queue.qsize() != 0:
            ms = MSSQL()
            task=queue.get(block=True, timeout=2)
            parser = MsgParser()
            try:
                dataList = parser.parse(task)
                #save as db
                insertsql = parser.constr(dataList)
                id = ms.executeAndGetId(insertsql)
                logger.info("Message has been inserted into db successfully, id: " + str(id))
                
                #send to application module
                notice_queue= GlobalParams.getNoticeProcessThread()
                notice_queue.put(id)

            except Exception, e:
                #log as file
                logger.error("Error occured!!!",exc_info=True)

