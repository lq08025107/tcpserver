from MyQueue import queue
import datetime
from MsgParserBox import MsgParser
from utiltool.DBOperator import MSSQL
import GlobalParams



def store():
    
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
                print id            
                print "insert into db successfully"
                
                #send to application module
                notice_queue= GlobalParams.getNoticeProcessThread()
                notice_queue.put(id)
                print "notice queue now has %d message" % notice_queue.qsize()

            except Exception, e:
                print "------------------------------------"
                print Exception, ":" , e
                #print task
                #log as file
                file = open("D:/tcp.txt",'a')
                now = datetime.datetime.now()
                file.write(now.strftime('%Y-%m-%d %H:%M:%S')+ ' |  ' +task)
                file.write('\n')
                file.close()
                print "------------------------------------"
            print queue.qsize()