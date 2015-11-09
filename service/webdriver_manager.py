from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import *
from service.logger_manager import logger
from config.config_loader import appConfig

class WebdriverManger(object):

    def __init__(self, *args, **kwargs):
        self.driver = self.__buildSeleniumDriver(*args, **kwargs)

    def __enter__(self):
        return self.driver

    def __exit__(self, exc_type, exc_value, traceback):
        self.closeAll()
        self.quitALL()

    def closeAll(self):
        self.driver.close()

    #end the session
    def quitALL(self):
        self.driver.quit()
        self.driver = None

    def getDriver(self):
        return self.driver

    def __buildSeleniumDriver(self, *args, **kwargs):

        #override if proxy is given
        proxy = None
        if "proxy_manager" in kwargs:
            proxy=kwargs["proxy_manager"].getWebDriverProxy()
        elif "proxy_host" in appConfig.selenium and "proxy_port" in appConfig.selenium:
            proxyIP = str(appConfig.selenium.proxy_host) + ":" + str(appConfig.selenium.proxy_port)
            proxy = Proxy({
                'proxyType': ProxyType.MANUAL,
                'httpProxy': proxyIP,
                'ftpProxy': proxyIP,
                'sslProxy': proxyIP,
                'noProxy': '' # set this value as desired
            })

        profile = webdriver.FirefoxProfile()
        # Set all new windows to open in the current window instead
        profile.set_preference('browser.link.open_newwindow', 1)
        # Disable all images from loading, speeds page loading
        # http://kb.mozillazine.org/Permissions.default.image
        #profile.set_preference('permissions.default.image', 2)
        # Disable stylesheet
        #profile.set_preference('permissions.default.stylesheet', 2)
        # Disable flashplayer
        #profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
        profile.set_preference('intl.accept_languages', 'en-us,en')
        profile.update_preferences()

        #determine driver using local or remote
        driver = None
        if appConfig.selenium.type == "remote":

            # for remote
            caps = webdriver.DesiredCapabilities.FIREFOX.copy()
            caps['javascriptEnabled'] = False
            caps['platform'] = 'ANY'
            caps['browserName'] = "firefox"
            caps['version'] = ''

            if proxy is not None:
                proxy.add_to_capabilities(caps)

            settings = {
                "command_executor" : appConfig.selenium.remote_server_path,
                "desired_capabilities" : caps
            }

            if profile is not None:
                settings["browser_profile"] = profile # NOTICE: firefox_profile is only available for firefox

            driver = webdriver.Remote(**settings)

        elif appConfig.selenium.type == "local":

            #for local
            settings = {}
            if proxy is not None:
                settings["proxy"] = proxy

            if profile is not None:
                settings["firefox_profile"] = profile # NOTICE: firefox_profile is only available for firefox

            driver = webdriver.Firefox(**settings)
        else:
            raise Exception("Unknown selenium.type {type}".format(type=appConfig.selenium.type))

        if "timeout" in kwargs:
            driver.set_page_load_timeout(kwargs["timeout"])

        return driver
