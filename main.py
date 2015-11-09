from service import PymongoManger, ProxyPool, UserPool, WebdriverManger, ProxyManager
from web_automation.abstract_web_action import AbstractWebAction
from web_automation.email_action.y28mail import Y28Mail
from web_automation.email_action.hotmail import HotMail
from web_automation.web_action.pixiv import Pixiv
from web_automation.web_action.anonymity_check.iprivacytools import Iprivacytools
from web_automation.web_action.basic.basic_web_action import BasicWebAction
from config.config_loader import appConfig
from service.logger_manager import logger
import time
import signal
import sys
import traceback

default_country = "jp"

proxy_pool = ProxyPool()
proxy_pool.initCollection()
proxy_pool_criteria = {
    "proxy_type" : "https",
    "anonymity_level" : { "$gte" : 2 },
    #"country" : { '$in':["jp", "hk", "tw","kr","us"] }
    "country" : default_country
}
proxy_pool.initPool(criteria=proxy_pool_criteria)

user_pool = UserPool()
user_pool.initCollection()
user_pool_criteria = {
    #"web_accounts.domain" : { "$ne" : "hotmail.com" }
    "web_accounts.domain" : { "$ne" : "y28mail.com" },
    #web_accounts.domain" : "y28mail.com",
    "country": default_country
}
user_pool.initPool(criteria=user_pool_criteria)

#Tor
web_action_proxy = ProxyManager("socks","127.0.0.1:9050")
AbstractWebAction.setProxyManager(web_action_proxy)
webdriver_proxy = ProxyManager("socks","127.0.0.1:9150")

wd_mgr = None
def signal_handler(signal, frame):
    print('Gracefully shutting down from SIGINT (Ctrl+C)')
    if wd_mgr is not None:
        wd_mgr.closeAll()
        wd_mgr.quitALL()

    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

while(not user_pool.isEmptyPool()):
    user = user_pool.getUser()

    attempt_count = 0
    is_finish = False
    while(not attempt_count > 2 and not is_finish):

        attempt_count+=1
        # Proxy pool
        # http_proxy = proxy_pool.getRandomProxy()
        # web_action_proxy.setHostname(http_proxy["hostname"])
        # web_action_proxy.setProtocol("http")
        # webdriver_proxy.setHostname(http_proxy["hostname"])
        # webdriver_proxy.setProtocol("http")

        try:
            with WebdriverManger(proxy_manager=web_action_proxy) as driver:
                Iprivacytools(driver).checkHTTP()#sleep_seconds=3)

                #is_finish = GoToURL(driver).go("")
                #is_finish = HotMail(driver).createAccount(user)
                while(not is_finish):
                    is_finish = Y28Mail(driver).createAccount(user)
                #is_finish = Pixiv(driver).createAccount(user)
                #Pixiv(driver).login(user)
        except Exception, e:
            is_finish = False
            tb = traceback.format_exc()
            logger.error("Error: \n%s" % e)
            logger.error("Stack Trace: \n%s" % tb)
            time.sleep(1)


