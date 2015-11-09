from service.pymongo_manager import PymongoManger
from config.config_loader import appConfig
from service import PymongoManger
from random import randrange
import pymongo
from service.user import User
from service.logger_manager import logger

class UserPool(object):

    def __init__(self):
        self.db = PymongoManger().getNew()
        self.user_pool = None
        self.initCollection()
        self.total_pool_size = 0

    def initCollection(self):
        allUninitRecord = self.db.users.find()
        self.poolCount = allUninitRecord.count()

        for uninitRecord in allUninitRecord:
            recordId = uninitRecord["_id"]

            updateSet = {}

            if len(updateSet) is 0:
                continue

            self.db.users.update(
                {"_id": recordId},
                {"$set":updateSet}
            )

    def initPool(self,criteria={}):
        self.user_pool = list(self.db.users.find(criteria))

        self.total_pool_size = len(self.user_pool)
        logger.debug("Initialized user pool size: %d" % self.total_pool_size)

        return len(self.user_pool)

    def isEmptyPool(self):
        return len(self.user_pool) is 0

    def getUser(self,reuse=False):
        if self.user_pool is None:
            raise Exception("User pool is not initialized")

        if self.isEmptyPool():
            raise Exception("User pool is empty")

        user = None
        isValidProxy = False
        pool_size = len(self.user_pool)
        rand = randrange(0,pool_size)

        user = None
        if reuse:
            user =  User(self.user_pool[rand])
        else:
            user =  User(self.user_pool.pop(rand))

        user.setUsersCollection(self.db.users)

        logger.debug("Use user: " + user.default_username)
        logger.info("Remaining user pool size: %d / %d" % (len(self.user_pool),self.total_pool_size))

        return user
