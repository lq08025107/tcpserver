import threading
from TCPServer import tw
from FTPServer import ftp
from MyQueue import queue
import datetime
from MsgParserBox import MsgParser
from DBOperator import MSSQL
#two thread to run twisted and ftp server
threads = []

ms = MSSQL(host="10.25.18.9",user="sa",pwd="p@ssw0rd",db="IVAS")
file = open("D:/tcp.txt",'a')
t1 = threading.Thread(target = tw)
threads.append(t1)

#t2 = threading.Thread(target = ftp)
#threads.append(t2)

for t in threads:
    t.start()

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
            print task
            #log as file
            
            now = datetime.datetime.now()
            file.write(now.strftime('%Y-%m-%d %H:%M:%S')+ ' |  ' +task)
            file.write('\n')
            print "------------------------------------"
        print queue.qsize()




