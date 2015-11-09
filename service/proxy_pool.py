from random import randrange
from selenium.webdriver.common.proxy import Proxy, ProxyType
import pymongo
import requests
import datetime
import time

from config import appConfig
from service import *
from service.logger_manager import logger

class ProxyPool(object):

  def __init__(self,db=appConfig.mongo.proscraper_database):
    self.db = PymongoManger(db=db).getNew()
    self.proxy_pool = None
    self.total_pool_size = 0

  def initCollection(self):
    allUninitRecord = self.db.web_proxys.find()
    self.poolCount = allUninitRecord.count()
    #   {"$or":[
    #     { "random_id" : { "$exists" : False } },
    #     { "associated_users" : { "$exists" : False } },
    #     { "proxy_pool_connectable" : { "$exists" : False } }
    #   ]}
    # )
    for uninitRecord in allUninitRecord:
      recordId = uninitRecord["_id"]

      updateSet = { }
      if "proxy_pool_connectable" not in uninitRecord:
        updateSet["proxy_pool_connectable"] = None

      if "proxy_pool_check_date" not in uninitRecord:
        updateSet["proxy_pool_check_date"] = None
      # if "associated_users" not in uninitRecord or len(uninitRecord["associated_users"]) is 0:
      #   updateSet["associated_users"] = []

      if len(updateSet) is 0:
        continue

      self.db.web_proxys.update(
        {"_id": recordId},
        {"$set":updateSet}
      )
    # self.db.web_proxys.create_index([("random_id", pymongo.ASCENDING)],unique=False)

  def initPool(self,criteria={}):

    if "anonymity_level" in criteria and not (isinstance( criteria["anonymity_level"], int ) or isinstance(criteria["anonymity_level"], dict)):
      raise Exception("anonymity_level must be int or dict")

    criteria["proxy_pool_connectable"] = { '$in':[True, None] }

    self.proxy_pool = list(self.db.web_proxys.find(criteria))

    self.total_pool_size = len(self.proxy_pool)
    logger.debug("Initialized proxy pool size: %d" % self.total_pool_size)

    return len(self.proxy_pool)

  def validateProxy(self,proxy):
    shoudRetry = True;
    attemptCount = 1
    while(shoudRetry):
        hostname = proxy["hostname"]
        country = proxy["country"]
        anonymity_level = proxy["anonymity_level"]
        proxy_type = proxy["proxy_type"]
        try:
            if proxy["proxy_type"] == "https":
              url = "https://example.com/"
            else:
              url = "http://example.com/"

            http_proxy  = "http://" + hostname
            https_proxy = "https://" + hostname
            ftp_proxy   = "ftp://" + hostname

            proxyDict = {
                          "http"  : http_proxy,
                          "https" : https_proxy,
                          "ftp"   : ftp_proxy
                        }

            r = requests.get(url, proxies=proxyDict, timeout=5)

            #if the above code does not throw timeout exception
            self.db.web_proxys.update(
              {"hostname":hostname},
              {"$set":{
                "proxy_pool_connectable": True,
                "proxy_pool_check_date": datetime.datetime.utcnow()
              }}
            )

            logger.debug("Use proxy:\n    hostname: %s\n    from: %s\n    anonymity_level: %s\n    proxy_type: %s\n" % (hostname,country,anonymity_level,proxy_type))
            logger.debug("Remaining proxy pool size: %d / %d" % (len(self.proxy_pool),self.total_pool_size))

            return True

        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError,TypeError) as e:
            # retry if the record is scraped freshly

            scraped_date = proxy["update_at"]
            now = datetime.datetime.now()
            timediff = now - scraped_date
            if timediff.days >= 1 or attemptCount >= 3:
              self.db.web_proxys.update(
                {"hostname":hostname},
                {"$set":{
                  "proxy_pool_connectable": False,
                  "proxy_pool_check_date": datetime.datetime.utcnow()
                }}
              )

              logger.debug("Invalidated proxy: %s (%s)" % (hostname,country))
              logger.debug("Invalidated reason:\n%s " % e.message)
              logger.debug("Remaining proxy pool size: %d / %d" % (len(self.proxy_pool),self.total_pool_size))

              return False
            else:
              #retry
              logger.debug("retry proxy: %s (%s)" % (hostname,country))
              attemptCount+=1
              time.sleep(1)

        # except requests.exceptions.TooManyRedirects:
        #     # Tell the user their URL was bad and try a different one
        # except requests.exceptions.RequestException as e:
        #     # catastrophic error. bail.

  def isEmptyPool(self):
        return len(self.proxy_pool) is 0

  def getRandomProxy(self,is_proxy_reuse=False):
    if self.proxy_pool is None:
        raise Exception("proxy pool is not initialized")

    if self.isEmptyPool():
        raise Exception("proxy pool is empty")

    proxy = None
    is_proxy_connectable = False
    while(not is_proxy_connectable):

      pool_size = len(self.proxy_pool)

      if pool_size is 0:
        raise Exception("proxy pool is empty")

      rand_index = randrange(0,pool_size)
      if is_proxy_reuse:
        proxy = self.proxy_pool[rand_index]
      else:
        proxy = self.proxy_pool.pop(rand_index)

      is_proxy_connectable = self.validateProxy(proxy)

      if not is_proxy_connectable and is_proxy_reuse:
        #remove the bad proxy from reusable proxy pool
        self.proxy_pool.pop(rand_index)

    return proxy
