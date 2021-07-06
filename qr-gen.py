#! /usr/bin/env python3
"""qr-gen.py
Small script that generates a QR image based on data being passed as
an argument.
"""

# Imports
import argparse
import os
import random
import sys
from string import ascii_letters, digits

import pyperclip
from cairosvg import svg2png
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from qrcodegen import QrCode, DataTooLongError

__author__ = "Shino"
__license__ = "GPL"
__version__ = "0.2"


CHAR_SET = ascii_letters + digits

class QrDisplay(QWidget):
    """QrDisplay: Class that creates and presentsa QR Code based on data passed
    either by an argument or in the clipboard.
    The qr image is saved on the temp directory,where it is fetched by showUi()
    """    
    def __init__(self):
        super().__init__()
        self.title = 'QR Code Viewer'
        self.left = 200
        self.top = 200
        self.width = 400
        self.height = 400

    def createRandomName(self):
        return ''.join(random.choices(population=CHAR_SET, k=8)) + '.png'

    def findTmp(self):
        """Finds the temporary folder, based on system platform

        Returns:
            str: absolute temp path
        """        
        plat = sys.platform
        if plat == 'linux' or plat == 'darwin':
            return '/tmp/'
        elif plat == 'win32':
            return os.getenv('TMP')
            
    
    def showUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        lbl = QLabel(self)
        pixmap = QPixmap(self.fn)
        lbl.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())

        self.show()


    def makeQrImage(self, data=None):
        """Creates the QR code.
        Data is provided either by an argument, or already in self.data 

        Args:
            data (str, optional): data to generate the qr code. Defaults to None.

        Raises:
            Exception: If no data is passed and there is None in self.data
        """        
        if data is None and self.data is None:
            raise Exception('No data found.')
        if data is not None:
            self.data = data
        
        try:        
            svg = QrCode.encode_text(self.data, QrCode.Ecc.LOW).to_svg_str(2)
        except DataTooLongError:
            print('Size of the data is too big. Please lower it')
            sys.exit(1)
            
        self.fn = self.findTmp() + self.createRandomName()
        svg2png(svg,scale=10, write_to=self.fn)

    def getClipboard(self):
        self.data = pyperclip.paste()

if __name__ == '__main__':
    args = argparse.ArgumentParser()
    req = args.add_mutually_exclusive_group(required=True)
    req.add_argument('-t','--text', dest='text', action='store')
    req.add_argument('-c', '--clipboard', dest='clip', action='store_true')

    p = args.parse_args()

    app = QApplication(sys.argv)
    ex = QrDisplay()
    
    if p.text:
        ex.makeQrImage(p.text)
    elif p.clip:
        ex.getClipboard()
        ex.makeQrImage()
        
    ex.showUI()
    sys.exit(app.exec_())

