from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import *
import time
from web_helper.password_generator.password_generator import PasswordGenerator
from service.proxy_manager import ProxyManager
import requests
# usr = "erickwok@hkitrade.net"
# pwd = "erickwok"

# myProxy = "36.238.87.236:3128"

# proxy = Proxy({
#     'proxyType': ProxyType.MANUAL,
#     'httpProxy': myProxy,
#     'ftpProxy': myProxy,
#     'sslProxy': myProxy,
#     'noProxy': '' # set this value as desired
#     })

# #for local
# #driver = webdriver.Firefox(proxy=proxy)

# # for remote
# caps = webdriver.DesiredCapabilities.FIREFOX.copy()
# proxy.add_to_capabilities(caps)

# # you have to use remote, otherwise you'll have to code it yourself in python to
# # dynamically changing the system proxy preferences

# driver = webdriver.Remote(command_executor='http://192.168.33.1:4444/wd/hub',desired_capabilities=caps)
# #driver = webdriver.Firefox()

# driver.get("https://myip.com.tw/")
# # driver.get("http://www.facebook.com")
# # assert "Facebook" in driver.title
# # elem = driver.find_element_by_id("email")
# # elem.send_keys(usr)
# # elem = driver.find_element_by_id("pass")
# # elem.send_keys(pwd)
# # elem.send_keys(Keys.RETURN)

# # time.sleep(10)
# # driver.get("http://198.211.105.112/like_button.html")
# # fb_like_div = driver.find_elements_by_class_name("fb-like")
# time.sleep(10)
# # action = webdriver.ActionChains(driver).move_to_element(fb_like_div).click()
# # action.perform()

# driver.close()

# import tempfile
# f = tempfile.NamedTemporaryFile(delete=False,suffix=None)
# f.close()
# print f.name

#print ProxyManager("http","165.139.149.169:3128").getRequestsResponse("http://myip.com.tw/", timeout=30).text




print requests.get("http://myip.com.tw/", timeout=5).content
