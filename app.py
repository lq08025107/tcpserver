import threading
from HTTPServer import http_tcp
from FTPServer import ftp
from Store import store
import GlobalParams
# thread to run twisted and ftp server
threads = []

#application module
GlobalParams.initProcessThread()

#http server
t1 = threading.Thread(target = http_tcp)
threads.append(t1)

#ftp server
#t2 = threading.Thread(target = ftp)
#threads.append(t2)

#store to db
t3 = threading.Thread(target = store)
threads.append(t3)



for t in threads:
    t.start()






