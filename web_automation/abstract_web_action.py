import urllib
import os
from contextlib import contextmanager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import staleness_of
from datetime import datetime
from selenium.common.exceptions import TimeoutException
from config.config_loader import appConfig
import time
import ntpath
import tempfile
from web_helper.user_interaction.wait_user_done import waitUserDone
from web_helper.user_interaction.wait_user_answer import waitUserAnswer

class DriverBehaveUnexpectedError(Exception):
    def __init__(self,*args,**kwargs):
        # Call the base class constructor with the parameters it needs
        super(DriverBehaveUnexpectedError, self).__init__(*args,**kwargs)

class DriverTimeoutError(Exception):
    def __init__(self,*args,**kwargs):
        # Call the base class constructor with the parameters it needs
        super(DriverTimeoutError, self).__init__(*args,**kwargs)

class AbstractWebAction(object):

    proxy_manager = None

    @classmethod
    def setProxyManager(klass,proxy_manager):
        klass.proxy_manager = proxy_manager

    #strict: no
    def __init__(self, driver,use_proxy_for_download=True):
        self.driver = driver
        self.tempfiles = []
        self.use_proxy_for_download = use_proxy_for_download

    @property
    def page_source(self):
        return self.driver.page_source.encode('utf-8')

    """ helper to raise common error """
    def raiseBehaveUnexpectedError(self,msg):
        self.save_screen()
        raise DriverBehaveUnexpectedError(msg)

    def raiseDriverTimeoutError(self,msg):
        self.save_screen()
        raise DriverTimeoutError(msg)

    """ helper to do stuff with driver """

    def getDriver(self):
        return self.driver

    def download(self,fromURL,filename,timeout=10):
        path = os.path.join(appConfig.root,'tmp',filename)

        if self.use_proxy_for_download is True:

            if self.proxy_manager is None:
                raise Exception("AbstractWebAction.proxy_manager is not set yet, or try to set use_proxy_for_download=False in constructor")

            # response = self.proxy_manager.getRequestsResponse(fromURL,timeout=timeout)
            # with open(path, 'wb') as f:
            #     f.write(response.content)
            #     f.close()

            response_value = self.proxy_manager.getCurlValue(fromURL,timeout=timeout)
            with open(path, 'wb') as f:
                f.write(response_value)
                f.close()
        else:
            #this will leak the real ip
            urllib.urlretrieve(fromURL, path)
        return path

    @contextmanager
    def temp_downloaded(self,fromURL,suffix="",timeout=10):
        file_path = self.download_as_temp(src,suffix=suffix)
        yield file_path
        self.clean_all_temp()

    #REMEMBER to call cleanAllTemp() after downAsTemp()
    def download_as_temp(self,fromURL,suffix="",timeout=10):
        path = self.__newTempFile(suffix=suffix)

        if self.use_proxy_for_download is True:

            if self.proxy_manager is None:
                raise Exception("AbstractWebAction.proxy_manager is not set yet, or try to set use_proxy_for_download=False in constructor")

            # response = self.proxy_manager.getRequestsResponse(fromURL,timeout=timeout)
            # with open(path, 'wb') as f:
            #     f.write(response.content)
            #     f.close()

            response_value = self.proxy_manager.getCurlValue(fromURL,timeout=timeout)
            with open(path, 'wb') as f:
                f.write(response_value)
                f.close()
        else:
            #this will leak the real ip
            urllib.urlretrieve(fromURL, path)
        return path

    def __newTempFile(self,**kwargs):
        f = tempfile.NamedTemporaryFile(**kwargs)
        self.tempfiles.append(f)
        path = f.name
        return path

    def clean_all_temp(self):
        while self.tempfiles:
            tempfile = self.tempfiles.pop(0)
            tempfile.close()

    def get_src_basename(self,src):
        return ntpath.basename(src);

    def save_screen(self,filename = None):
        if filename is None:
            filename = datetime.now().strftime("%Y-%m-%d--%H-%M-%S-%f")
        screenshotPath = os.path.join(appConfig.root,'log','screenshot','{filename}.png'.format(filename=filename))
        self.driver.save_screenshot(screenshotPath)
        return screenshotPath



    def sleep(self,seconds=1):
        time.sleep(seconds)

    def sleep_like_click(self):
        time.sleep(0.6)

    def wait_done(self,timeout=30):
        waitUserDone(self).waitUntilDone(timeout)

    def wait_answer(self,timeout=30):
        return waitUserAnswer(self).waitUntilAnswer(timeout)

    def load(self,url,timeout=30):
        with self.wait_page_update(timeout=timeout):
            self.driver.get(url)

    """
    example:

    with self.wait_for_page_load(timeout=10):
            self.driver.find_element_by_link_text('a link').click()

    Note that this solution only works for "non-javascript" clicks,
    ie clicks that will cause the browser to load a brand new page,
    and thus load a brand new HTML body element.
    """
    @contextmanager
    def wait_page_update(self, timeout=30):
        old_page = self.driver.find_element_by_tag_name('html')
        yield
        try:
            WebDriverWait(self.driver, timeout).until(
                staleness_of(old_page),"timeout"
            )
        except TimeoutException,e:
            self.raiseDriverTimeoutError('driver timeout with url: {url}'.format(url=self.driver.current_url))
