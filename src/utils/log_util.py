import logging
import logging.handlers
import os
from concurrent_log import ConcurrentTimedRotatingFileHandler

class LogUtil:
    # ��ʼ����־
    def __init__(self):
        self.logPath = 'data/log/'
        self.logName = 'buff_player.log'
        self.logFile = self.logPath + self.logName

        self.log_path = os.getcwd() + os.sep + self.logPath
        if not os.path.isdir(self.log_path):
            os.makedirs(self.log_path)

        concurrent_handler = ConcurrentTimedRotatingFileHandler(self.logFile, when='H', interval=1,
                                                                      backupCount=168, encoding='utf-8',
                                                                      errors='ignore')
        # concurrent_handler = logging.handlers.TimedRotatingFileHandler(self.logFile, when='H', interval=1,
        #                                                               backupCount=168, encoding='latin-1',
        #                                                               errors='ignore')

        concurrent_handler.suffix = "buff_player.log.%Y%m%d%H"
        # formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s:  %(message)s')
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
        concurrent_handler.setFormatter(formatter)

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)

        handler_list = []
        handler_list.append(concurrent_handler)
        handler_list.append(stream_handler)

        # ��־�������ʽ
        logging.basicConfig(
            level = logging.INFO,  # ����CRITICAL > ERROR > WARNING > INFO > DEBUG��Ĭ�ϼ���Ϊ WARNING
            format = '%(asctime)s [%(levelname)s] %(message)s',
            encoding = 'latin-1', errors = 'ignore',
            handlers = handler_list)




    @staticmethod
    def debug(content):
        logging.debug(content)
        # ����д�����ĺ���,ʹ�����������log

    @staticmethod
    def error(content):
        logging.error(content)

    @staticmethod
    def info(content):
        logging.info(content)

    @staticmethod
    def warning(content):
        logging.warning(content)