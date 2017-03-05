#coding=utf-8
import logging, os
import ConfigParser
class Logger:
    instance = None
    def __init__(self, path = 'log.txt', clevel = logging.DEBUG, flevel = logging.DEBUG):
        self.logger = logging.getLogger(path)
        self.logger.setLevel(logging.DEBUG)
        self.format = '%(asctime)s %(filename)s[line:%(lineno)d] %(threadName)s %(levelname)s %(message)s'
        self.datefmt = '%a, %d %b %Y %H:%M:%S'
        fmt = logging.Formatter(self.format, self.datefmt)
        #for cosole log
        sh = logging.StreamHandler()
        sh.setFormatter(fmt)
        cp = ConfigParser.SafeConfigParser()
        cp.read('processcore/db.ini')
        clevel = (int)(cp.get('log', 'level'))
        sh.setLevel(clevel)
        #for file log
        fh = logging.FileHandler(path)
        fh.setFormatter(fmt)
        fh.setLevel(flevel)
        self.logger.addHandler(sh)
        self.logger.addHandler(fh)

    @classmethod
    def getInstance(cls):
        if cls.instance:
            return cls.instance
        else:
            cls.instance = Logger().logger
            return cls.instance

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warn(self, message):
        self.logger.warn(message)

    def error(self, message):
        self.logger.error(message)

if __name__ == '__main__':
    loggera = Logger()
    loggera.debug('aa')