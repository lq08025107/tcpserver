import threading
from HTTPServer import http
from FTPServer import ftp
from Store import store
#two thread to run twisted and ftp server
threads = []


t1 = threading.Thread(target = http)
threads.append(t1)

#t2 = threading.Thread(target = ftp)
#threads.append(t2)

t3 = threading.Thread(target = store)
threads.append(t3)
for t in threads:
    t.start()






