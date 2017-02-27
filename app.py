import threading
from Reactor import start_reactor
from FTPServer import ftp
from Store import start_store
import GlobalParams
from HTTPServer import start_http
# thread to run twisted and ftp server
threads = []

#application module
GlobalParams.initProcessThread()
#store to db

#http server
t1 = threading.Thread(target = start_reactor)
threads.append(t1)

#ftp server
#t2 = threading.Thread(target = ftp)
#threads.append(t2)

t3 = threading.Thread(target = start_store)
threads.append(t3)

for t in threads:
    t.start()






