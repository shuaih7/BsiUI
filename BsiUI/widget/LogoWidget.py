#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 04.20.2021
Updated on 04.23.2021

Author: haoshuai@handaotech.com
'''

import os
import sys
import copy
import numpy as np
from PIL import Image
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QImage, QPixmap, QPainter


file_path = os.path.abspath(os.path.dirname(__file__))
abs_path = os.path.abspath(os.path.join(file_path, '..'))
sys.path.append(abs_path)


class LogoWidget(QLabel):
    def __init__(self, parent=None):
        super(LogoWidget, self).__init__(parent)
        self.pixmap = None
        
    def setConfig(self, params):
        icon_path = os.path.join(abs_path, 'icon')
        logo_file = os.path.join(icon_path, params['logo_file'])
        self.img = Image.open(logo_file)
        self.updatePixmap()
        self.params = params
        
    def resizeWidget(self, size):
        off_w = int(self.params['off_w'])
        off_h = int(self.params['off_h'])
        ratio_w = float(self.params['ratio_w'])
        ratio_h = float(self.params['ratio_h'])
        
        width = int(size.width() * ratio_w)
        height = int(size.height() * ratio_h)
        self.setGeometry(off_w, off_h, width, height)
        self.updatePixmap()
                
    def updatePixmap(self):
        img_w, img_h = self.img.size
        img_aspect_ratio = img_w / img_h
        width, height = self.width(), self.height()
        aspect_ratio = width / height
        
        img = copy.deepcopy(self.img)
        if aspect_ratio > img_aspect_ratio: # Keep aspect ratio
            img = img.resize((int(height*img_aspect_ratio), height), 
                resample=Image.BILINEAR)
        else:
            img = img.resize((width, int(width/img_aspect_ratio)), 
                resample=Image.BILINEAR)
                
        image = np.array(img, dtype=np.uint8)
        h, w, ch = image.shape[:3]
        bytesPerLine = ch*w
        convertToQtFormat = QImage(image.data.tobytes(), w, h, bytesPerLine, QImage.Format_RGBA8888)
        self.pixmap = QPixmap.fromImage(convertToQtFormat).scaled(self.size(), Qt.KeepAspectRatio, 
            Qt.SmoothTransformation)
        
    def paintEvent(self, event):
        if self.pixmap is None: return
        
        painter = QPainter(self)
        #off_x = (self.size().width() - self.pixmap.width()) / 2
        off_y = (self.size().height() - self.pixmap.height()) / 2
        painter.drawPixmap(0, off_y, self.pixmap)