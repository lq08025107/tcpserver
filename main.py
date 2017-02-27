from threading import Thread
import TCPServerModule

import TCPServerModule
import GlobalParams

GlobalParams.initProcessThread()
tr = Thread(target = TCPServerModule.startTCPServerMoudule)
tr.start()

# while True:
#     a = raw_input()
#     xmlfile = open(".//.RESOURCE//XMLBuild.xml")
#     data = xmlfile.read()
#     np= GlobalParams.getNoticeProcessThread()
#     np.put(data)