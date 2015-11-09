import pymongo

from config.config_loader import appConfig
from service.logger_manager import logger

class PymongoManger(object):

    def __init__(self, *args, **kwargs):
        self.conn = None
        if "db" in kwargs:
            self.db = kwargs["db"]
        else:
            self.db = appConfig.mongo.database

    def getNew(self, *args, **kwargs):
        if self.conn is None:
            self.conn = self.__buildConn(*args, **kwargs)

        db = self.__getDBObject(self.conn, *args, **kwargs)
        return db

    def closeAll(self):
        self.conn.close()

    def __getDBObject(self,conn,*args, **kwargs):
            return conn[self.db]

    def __buildConn(self, *args, **kwargs):
        try:
            conn=None
            if "host" in appConfig.mongo and "port" in appConfig.mongo:
                conn = pymongo.MongoClient(host=appConfig.mongo.host, port=appConfig.mongo.port)
            else:
                conn = pymongo.MongoClient()
            return conn
        except pymongo.errors.ConnectionFailure, e:
            logger.error("Could not connect to MongoDB: %s" % e )
            raise
