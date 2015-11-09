import sys
import os
import re
import subprocess
import tempfile
from PIL import Image
import logging
import ntpath
import tempfile

from service.logger_manager import LoggerManager

class TesseractCaptchaParser():

    def __call_command(self,*args):
        """call given command arguments, raise exception if error, and return output"""
        c = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = c.communicate()
        if c.returncode != 0:
            if error:
                raise Exception(error)
            self.logger.error("Error running `%s'" % ' '.join(args))
        return output

    def __init__(self):
        self.logger = LoggerManager.getInstance()
        self.tempfiles = []

        #check if tesseract is installed
        self.__call_command('tesseract','-v')

    def __cleanAllTemp(self):
        while self.tempfiles:
            tempfile = self.tempfiles.pop(0)
            tempfile.close()

    def __newTempFile(self,**kwargs):
        f = tempfile.NamedTemporaryFile(**kwargs)
        self.tempfiles.append(f)
        path = f.name
        return path

    def parse(self,filename):
        """Return the text for thie image using Tesseract"""
        img = self.__threshold(filename)
        result_string = self.__tesseract(img)
        self.__cleanAllTemp()
        return result_string

    def __threshold(self,filename, limit=100):
        """Make text more clear by thresholding all pixels above / below this limit to white / black"""
        # read in colour channels
        img = Image.open(filename)
        # resize to make more clearer
        m = 1.5
        img = img.resize((int(img.size[0]*m), int(img.size[1]*m))).convert('RGBA')
        pixdata = img.load()

        for y in xrange(img.size[1]):
            for x in xrange(img.size[0]):
                if pixdata[x, y][0] < limit:
                    # make dark color black
                    pixdata[x, y] = (0, 0, 0, 255)
                else:
                    # make light color white
                    pixdata[x, y] = (255, 255, 255, 255)
        #create a tempfile for threshold image file
        filename_without_extension, file_extension = os.path.splitext(filename)
        path= self.__newTempFile(prefix="threshold_",suffix=file_extension)
        #OR save it to other folder
        #img.save('tmp/threshold_' + ntpath.basename(filename))
        img.save(path)
        return img.convert('L') # convert image to single channel greyscale

    def __tesseract(self,image):
        """Decode image with Tesseract  """
        # create temporary file for tiff image required as input to tesseract
        input_file = tempfile.NamedTemporaryFile(suffix='.tif')
        image.save(input_file.name)

        # perform OCR
        output_filename = input_file.name.replace('.tif', '.txt')
        self.__call_command('tesseract', input_file.name, output_filename.replace('.txt', ''))

        # read in result from output file
        result = open(output_filename).read()
        os.remove(output_filename)
        return self.__clean(result)

    # def gocr(image):
        # """Decode image with gocr
        # """
        # input_file = tempfile.NamedTemporaryFile(suffix='.ppm')
        # image.save(input_file.name)
        # result = call_command('gocr', '-i', input_file.name)
        # return clean(result)


    # def ocrad(image):
        # """Decode image with ocrad
        # """
        # input_file = tempfile.NamedTemporaryFile(suffix='.ppm')
        # image.save(input_file.name)
        # result = call_command('ocrad', input_file.name)
        # return clean(result)

    def __clean(self,s):
        """Standardize the OCR output"""
        # remove non-alpha numeric text
        return re.sub('[\W]', '', s)



