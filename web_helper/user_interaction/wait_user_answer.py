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

class waitUserAnswer():

    def __init__(self,webAction):
        self.webAction = webAction
        self.driver = webAction.driver

    def __appendContinueLink(self,driver):
        js = """

        (function(){

            var result_node = document.createElement("a");
            var textnode = document.createTextNode("result not yet determined");
            result_node.appendChild(textnode);
            result_node.id = "wait-user-answer-result"
            result_node.style.margin = "auto"

            var true_node = document.createElement("A");
            var textnode = document.createTextNode("let's return True!");
            true_node.appendChild(textnode);
            true_node.style.fontSize = '18px';
            true_node.style.color    = 'black';
            true_node.style.float    = "left"
            true_node.href           = '#';
            true_node.onclick        = function(){ returnTrue() };

            var false_node = document.createElement("A");
            var textnode = document.createTextNode("Nono, return False!");
            false_node.appendChild(textnode);
            false_node.style.fontSize = '18px';
            false_node.style.color    = 'black';
            false_node.style.float    = "right";
            false_node.href           = '#';
            false_node.onclick        = function(){ returnFalse() };


            function returnTrue(){
                if(result_node !== undefined){
                    result_node.text = "=True"

                    true_node.text  = "Haha, True returned!"
                    false_node.text = "..."
                }
                result_node = undefined;
            }

            function returnFalse(){
                if(result_node !== undefined){
                    result_node.text = "=False"

                    true_node.text  = "..."
                    false_node.text = "Hoho, False returned!"
                }
                result_node = undefined;
            }

            var container = document.createElement("div");
            container.appendChild(true_node);
            container.appendChild(false_node);
            container.appendChild(result_node);
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

    def waitUntilAnswer(self,timeout = 30):
        """Return the text for thie image using Tesseract"""
        self.__appendContinueLink(self.driver)
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.find_element_by_id('wait-user-answer-result').text.startswith('='),"timeout"
            )
            return_text = self.driver.find_element_by_id('wait-user-answer-result').text
            if return_text == "=True":
                return True
            elif return_text == "=False":
                return False
        except TimeoutException,e:
            self.webAction.raiseDriverTimeoutError('wait user timeout')
            return


