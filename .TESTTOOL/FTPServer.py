from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer


authorizer = DummyAuthorizer()

authorizer.add_user("root", "sdt108", "D:/", perm="elradfmw")#adfmw

authorizer.add_anonymous("D:/", perm="elradfmw")
 
handler = FTPHandler
handler.authorizer = authorizer
def ftp():
    server = FTPServer(("10.25.18.30", 21), handler)
    server.serve_forever()