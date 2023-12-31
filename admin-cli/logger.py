import logging
import datetime

currentdatetime = datetime.datetime.now().strftime("%d-%m-%Y-%H:%M:%S")
logger = logging.getLogger('Python_Project')
loggerinit = False


def initdebuglogger():
    global logger, loggerinit
    if loggerinit:
        raise Exception("Logger was initialized twice")
    logger.setLevel(logging.DEBUG)
    ch, formatter = logging.FileHandler(".".join([currentdatetime, "log"])), logging.Formatter('[%(asctime)s] [%('
                                                                                               'name)s/%('
                                                                                               'levelname)s]: %('
                                                                                               'message)s')
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    loggerinit = True


def initapplogger():
    global logger, loggerinit
    if loggerinit:
        raise Exception("Logger was initialized twice")
    logger.setLevel(logging.INFO)
    ch, formatter = logging.FileHandler(".".join([currentdatetime, "log"])), logging.Formatter('[%(asctime)s] [%('
                                                                                               'name)s/%('
                                                                                               'levelname)s]: %('
                                                                                               'message)s')
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    loggerinit = True
