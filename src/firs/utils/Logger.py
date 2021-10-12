from .utils import singleton
import logging
import sys

class StreamToLogger(object):
    """
    Fake file-like stream object that redirects writes to a logger instance.
    """
    def __init__(self, logger, level):
       self.logger = logger
       self.level = level
       self.linebuf = ''

    def write(self, buf):
       for line in buf.rstrip().splitlines():
          self.logger.log(self.level, line.rstrip())

    def flush(self):
        pass


@singleton
class Logger:

    def __init__(self, **kwargs):

        #formatter = logging.Formatter(
        #    '%(asctime)s - %(name)s [%(module)s-%(funcName)s:%(lineno)d]- %(levelname)s - %(message)s')
        formatter = logging.Formatter(
            '%(asctime)s - [%(module)s:%(lineno)d]- %(levelname)s - %(message)s')

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)


        if 'loggerPath' in kwargs:
            loggingFile = kwargs['loggerPath']
            lhandler = logging.FileHandler(loggingFile, 'a')

        else:
            lhandler = logging.StreamHandler()

        lhandler.setFormatter(formatter)
        self.logger.addHandler(lhandler)

        #sys.stdout = StreamToLogger(self.logger, logging.DEBUG)
        #sys.stderr = StreamToLogger(self.logger, logging.ERROR)


