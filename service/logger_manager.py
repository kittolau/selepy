import os
import logging
import sys
from config.config_loader import appConfig

class LoggerManager(object):

    klassLogger = None

    @classmethod
    def getInstance(klass):
        return klass.__getLogger()

    @classmethod
    def __getLogger(klass):
        if klass.klassLogger is not None:
            return klass.klassLogger
        else:
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            klassLogger = logging.getLogger(appConfig.logger.name)

            #file handler
            if "file_log" in appConfig.logger:
                level = logging.getLevelName(appConfig.logger.file_log.level)
                klassLogger.setLevel(level)

                logPath = os.path.join(appConfig.root,'log',appConfig.logger.file_log.filename)
                hdlr = logging.FileHandler(logPath)

                hdlr.setFormatter(formatter)

                klassLogger.addHandler(hdlr)

            #std handler
            if "stdout_log" in appConfig.logger:
                ch = logging.StreamHandler(sys.stdout)

                level = logging.getLevelName(appConfig.logger.stdout_log.level)
                ch.setLevel(level)

                ch.setFormatter(formatter)

                klassLogger.addHandler(ch)

            klass.klassLogger = klassLogger
            return klass.klassLogger

logger = LoggerManager.getInstance();
