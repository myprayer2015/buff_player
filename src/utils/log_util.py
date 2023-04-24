import logging
import logging.handlers
import os
from concurrent_log import ConcurrentTimedRotatingFileHandler

class LogUtil:
    # 初始化日志
    def __init__(self):
        pass

    @staticmethod
    def init():
        logPath = 'data/log/'
        logName = 'buff_player.log'
        logFile = logPath + logName

        log_path = os.getcwd() + os.sep + logPath
        if not os.path.isdir(log_path):
            os.makedirs(log_path)

        concurrent_handler = ConcurrentTimedRotatingFileHandler(logFile, when='H', interval=1,
                                                                      backupCount=168, encoding='utf-8',
                                                                      errors='ignore')
        # concurrent_handler = logging.handlers.TimedRotatingFileHandler(logFile, when='H', interval=1,
        #                                                               backupCount=168, encoding='latin-1',
        #                                                               errors='ignore')

        concurrent_handler.suffix = "%Y%m%d%H"
        # formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s:  %(message)s')
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
        concurrent_handler.setFormatter(formatter)

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)

        handler_list = []
        handler_list.append(concurrent_handler)
        handler_list.append(stream_handler)

        # 日志的输出格式
        logging.basicConfig(
            level = logging.INFO,  # 级别：CRITICAL > ERROR > WARNING > INFO > DEBUG，默认级别为 WARNING
            format = '%(asctime)s [%(levelname)s] %(message)s',
            encoding = 'latin-1', errors = 'ignore',
            handlers = handler_list)



    @staticmethod
    def debug(content):
        logging.debug(content)
        # 可以写其他的函数,使用其他级别的log

    @staticmethod
    def error(content):
        logging.error(content)

    @staticmethod
    def info(content):
        logging.info(content)

    @staticmethod
    def warning(content):
        logging.warning(content)