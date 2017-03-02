from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from threading import Thread
from config import ServerConfig
from LogModule import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)

class FTPServerThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        logger.info("FTP " + self.getName() + " Start Running")
        authorizer = DummyAuthorizer()

        authorizer.add_user("root", "sdt108", "D:/", perm="elradfmw")#adfmw

        authorizer.add_anonymous("D:/", perm="elradfmw")

        handler = FTPHandler
        handler.authorizer = authorizer

        server = FTPServer((ServerConfig.FTPSERVERHOST, ServerConfig.FTPSERVERPORT), handler)
        server.serve_forever()
        logger.info("Store " + self.getName() + " Stop Run")