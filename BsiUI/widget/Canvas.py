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
from PIL import Image
from PyQt5.QtWidgets import QLabel, QApplication
from PyQt5.QtCore import Qt, QPoint, QRect, QLineF, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QColor


class Canvas(QLabel):
    def __init__(self, parent=None):
        super(Canvas, self).__init__(parent)
        self.image = None
        self.pixmap = None
        
    def setConfig(self, params):
        self.params = params
        
    def refresh(self, image_list):
        if not isinstance(image_list, list): return 
        
        image = self.concatImageList(image_list)
        
    def resize(self, size):
        off_w = int(self.params['off_w'])
        off_h = int(self.params['off_h'])
        
        width = max(10, size.width() - 2*off_w)
        height = max(10, size.height() - 2*off_h)
        self.setGeometry(off_w, off_h, width, height)
        
    def concatImageList(self, image_list):
        if len(image_list) == 0: return None
        elif len(image_list) == 1: return image_list[0]
        
        h, w = image_list[0].shape[:2]
        for i in range(1, len(image_list), 1):
            pass
            