import socket
import time
import random

def StructureWarnMsg(xmlpath = None):
    if xmlpath == None:
        xmlpath, xmltype = random.choice([(".//zcalarm.xml", "Video_Person"), (".//zcoveralarm.xml", "Video_Cover")])
    else:
        if xmlpath == ".//zcalarm.xml":
            xmltype = "Video_Person"
        else:
            xmltype = "Video_Cover"

    xmlfile = open(xmlpath)
    data = xmlfile.read()

    return data, xmltype

def main():
    host = 'localhost'
    port = 8800

    sendcount = 0

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    client.connect((host, port))
    data, type = StructureWarnMsg("..//.RESOURCE//OperatorSend.xml")
    # client.send(data)

    while True:
        print "11111"
        data = client.recv(1024)
        print data

main()



