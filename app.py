import threading
from TCPServer import tw
from FTPServer import ftp
#two thread to run twisted and ftp server
threads = []
t1 = threading.Thread(target = tw)
threads.append(t1)
t2 = threading.Thread(target = ftp)
threads.append(t2)
for t in threads:
    t.start()