from selenium.webdriver.common.proxy import Proxy, ProxyType
import socket
import socks
import re
import requests
import pycurl
import io

class ProxyManager(object):

    def __init__(self, protocol, hostname):
        self.setProtocol(protocol)
        self.setHostname(hostname)

    def setHostname(self,new_hostname):
        m = re.search("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+",new_hostname)
        if not m:
            raise Exception("%s is not a valid hostname" % new_hostname)
        self.hostname = new_hostname

    def setProtocol(self,new_protocol):
        if new_protocol != "http" and new_protocol != "socks":
            raise Exception("protocol should either be 'http' or 'socks'")
        self.protocol = new_protocol

    def getWebDriverProxy(self):
        hostname = self.hostname
        if self.protocol == "http":
            return Proxy({
                'proxyType': ProxyType.MANUAL,
                'httpProxy': hostname,
                'ftpProxy': hostname,
                'sslProxy': hostname,
                'noProxy': '' # set this value as desired
            })
        elif self.protocol == "socks":
            return Proxy({
                'proxyType': ProxyType.MANUAL,
                'socksProxy': hostname,
                'noProxy': '', # set this value as desired
            })

    def getRequestsResponse(self,url,timeout=5):
        hostname = self.hostname
        if self.protocol == "http":
            http_proxy  = "http://" + hostname
            https_proxy = "https://" + hostname
            ftp_proxy   = "ftp://" + hostname

            proxyDict = {
                          "http"  : http_proxy,
                          "https" : https_proxy,
                          "ftp"   : ftp_proxy
                        }
            return requests.get(url, timeout=timeout, proxies=proxyDict)
        elif self.protocol == "socks":
            default_socket = socket.socket

            ip, port = hostname.split(':')

            SOCKS5_PROXY_HOST = ip
            SOCKS5_PROXY_PORT = int(port)

            socks.set_default_proxy(socks.SOCKS5, SOCKS5_PROXY_HOST, SOCKS5_PROXY_PORT)
            socket.socket = socks.socksocket

            result = requests.get(url, timeout=timeout)

            #reset socket
            socket.socket = default_socket
            return result

    def getCurlValue(self,url,timeout=5):
        hostname = self.hostname
        ip, port = hostname.split(':')
        PROXY_HOST = ip
        PROXY_PORT = int(port)

        query = pycurl.Curl()
        query.setopt(pycurl.URL, url)
        query.setopt(pycurl.CONNECTTIMEOUT, timeout)
        query.setopt(pycurl.TIMEOUT, timeout)

        query.setopt(pycurl.PROXY, PROXY_HOST)
        query.setopt(pycurl.PROXYPORT, PROXY_PORT)

        query.setopt(pycurl.USERAGENT, 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)')

        output = io.BytesIO()
        query.setopt(pycurl.WRITEFUNCTION, output.write)

        if self.protocol == "http":
            query.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_HTTP)
        elif self.protocol == "socks":
            query.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5_HOSTNAME)

        query.perform()
        return output.getvalue()














