import sys
import os
import re
import subprocess
import tempfile
from PIL import Image
import logging
import ntpath

from service.logger_manager import logger
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

class waitUserDone():

    def __init__(self,webAction):
        self.webAction = webAction
        self.driver = webAction.driver

    def __appendContinueLink(self,driver):
        js = """

        (function(){
            var node = document.createElement("A");
            var textnode = document.createTextNode("I am done!");
            node.appendChild(textnode);
            node.style.fontSize = '18px';
            node.style.color = 'black';
            node.id             = 'i-am-done-with-it';
            node.href           = '#';
            node.onclick        = function(){ iAmDone() };

            function iAmDone(){
                node.text = "Done confirmed, proceeding..."
            }

            window.onkeyup = function(e) {
                var key = e.keyCode ? e.keyCode : e.which;

                //also add a done shortcut key using 'End' key
                if (key == 35) {
                    iAmDone();
                }
            }

            var container = document.createElement("div");
            container.appendChild(node);
            container.style.position        = 'fixed';
            container.style.bottom          = '0px';
            container.style.right           = '0px';
            container.style.width           = '100%';
            container.style.backgroundColor = 'yellow';
            container.style.textAlign       = 'center';
            container.style.zIndex          = '999';

            document.body.insertBefore( container, document.body.firstChild );
        }());

        """
        driver.execute_script(js)

    def waitUntilDone(self,timeout = 30):
        """Return the text for thie image using Tesseract"""
        self.__appendContinueLink(self.driver)
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.find_element_by_id('i-am-done-with-it').text.startswith('Done confirmed'),"timeout"
            )
        except TimeoutException,e:
            self.webAction.raiseDriverTimeoutError('wait user timeout')
            return


