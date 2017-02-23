from MyQueue import queue
import datetime
from MsgParserBox import MsgParser
from DBOperator import MSSQL

ms = MSSQL(host="10.25.18.9",user="sa",pwd="p@ssw0rd",db="IVAS")


def store():
    while(True):
        if queue.qsize() != 0:
            task=queue.get(block=True, timeout=2)
            parser = MsgParser()
            try:
                dataList = parser.parse(task)
                #save as db
                insertsql = parser.constr(dataList)
                ms.ExecNonQuery(insertsql)
                print "insert into db successfully"

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