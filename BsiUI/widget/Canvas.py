#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 04.20.2021
Updated on 04.20.2021

Author: haoshuai@handaotech.com
'''

import os
import cv2
import copy
import numpy as np
from PIL import Image
from PyQt5.QtWidgets import QLabel, QApplication
from PyQt5.QtCore import Qt, QPoint, QRect, QLineF, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QColor


class Canvas(QLabel):
    def __init__(self, parent=None):
        super(Canvas, self).__init__(parent)
        self.image = None
        self.pixmap = None
        self.scale = 1.0    # Concatenated image width / widget width, should be larger than 1
        self.center = QPoint(self.width()/2, self.height()/2)
        self.cursor = QPoint(self.width()/2, self.height()/2) # Cursor position
        
    def setConfig(self, params):
        self.params = params
        
    def refresh(self, image_list):
        if not isinstance(image_list, list): return 
        
        image = self.concatImageList(image_list)
        image = self.cropImage(image)
        image = self.resizeImage(image)
        
    def resizeWidget(self, size):
        off_w = int(self.params['off_w'])
        off_h = int(self.params['off_h'])
        
        width = max(10, size.width() - 2*off_w)
        height = max(10, size.height() - 2*off_h)
        self.setGeometry(off_w, off_h, width, height)
        
    def mousePressEvent(self, ev):
        pass
        
    def wheelEvent(self, ev):
        angle = ev.angleDelta().y()
        print(angle)
        
    def concatImageList(self, image_list):
        if len(image_list) == 0: return None
        elif len(image_list) == 1: return image_list[0]
        
        image_list = tuple(image_list)
        image_concat = np.hstack(image_list)
        
        return image_concat
        
    def cropImage(self, image):
        x, y = self.cursor.x(), self.cursor.y()
        height, width = image.shape[:2]
        
        #height = height * self.scale     # Resized image height
        #width = width * self.scale       # Resized image width
        
        left = int(max(0, x*self.scale))
        
        return image
        
    def resizeImage(self, image):
        
        return image
        
    def paintEvent(self, event):
        painter = QPainter(self)
        
        if self.pixmap is not None: 
            off_x = (self.size().width() - self.pixmap.width()) / 2
            off_y = (self.size().height() - self.pixmap.height()) / 2
            painter.drawPixmap(off_x, off_y, self.pixmap)
            
            