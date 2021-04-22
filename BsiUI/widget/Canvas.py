#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 04.20.2021
Updated on 04.22.2021

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


def format_image(image): # Gray to RGB
    if image.shape[-1] == 4: 
        image = image[:,:,:3]
    elif image.shape[-1] != 3: 
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)

    return image


class Canvas(QLabel):
    def __init__(self, parent=None):
        super(Canvas, self).__init__(parent)
        self.pixmap = None
        self.initParams()
    
    def initParams(self):
        self.scale = 1.0         # Concatenated image width / widget width, should be larger than 1
        self.scale_factor = 1.0  # Scale compared to the previous image
        self.is_register = False # Whether the image info has been regisgtered
        self.cursor = QPoint(self.width()/2, self.height()/2) # Cursor position
        
    def setConfig(self, params):
        self.zoom_factor = params['zoom_factor']
        self.max_scale = params['max_scale']
        self.params = params
        
    def refresh(self, image_list):
        if not isinstance(image_list, list): return 
        
        image = self.concatImageList(image_list)
        if not self.is_register: self.registerImageInfo(image)
        
        image = self.cropResizeImage(image)
        self.convertPixmap(image)
        self.update()
        
    def resizeWidget(self, size):
        off_w = int(self.params['off_w'])
        off_h = int(self.params['off_h'])
        
        width = max(10, size.width() - 2*off_w)
        height = max(10, size.height() - 2*off_h)
        self.setGeometry(off_w, off_h, width, height)
        
    def resizeContent(self, angle, position):
        x, y = position.x(), position.y()
        
        image_h, image_w = self.image_h, self.image_w        # Original image height and width
        disp_h = image_h * (self.scale*self.width()/image_w) # Image height displayed on the canvas
        disp_w = image_w * (self.scale*self.width()/image_w) # Image width displayed on the canvas
        
        # Update the scale and scale factor
        if angle > 0: scale = min(self.max_scale, self.scale*self.zoom_factor)
        else: scale = max(1.0, self.scale/self.zoom_factor)
        scale_factor = scale / self.scale
        
        # Update the over-widget pixels
        left_image_len = x + self.left_index # Distance from the cursor to the displayed image left boundary
        top_image_len = y + self.top_index   # Distance from the cursor to the displayed image top boundary
        
        self.left_index = max(0, int(left_image_len*scale_factor-x))
        if top_image_len < 0:
            self.top_index = int((disp_h - self.height)/2)
        else:
            self.top_index = int(top_image_len*scale_factor-y)
        
        self.scale = scale
        self.scale_factor = scale_factor
        self.cursor = position
        
    def registerImageInfo(self, image):
        assert self.scale == 1.0, 'Initial scale should be 1.0'
        self.image_h, self.image_w = image.shape[:2]
        widget_h, widget_w = self.height(), self.width()
        
        self.left_index = 0
        self.top_index = int((widget_h - (widget_w/self.image_w)*self.image_h) / 2) * -1
        self.is_register = True
        
    def mousePressEvent(self, ev):
        pass
        
    def wheelEvent(self, ev):
        angle = ev.angleDelta().y()
        position = ev.pos()
        self.resizeContent(angle, position)
        
    def concatImageList(self, image_list):
        if len(image_list) == 0: return None
        elif len(image_list) == 1: return image_list[0]
        
        image_list = tuple(image_list)
        image_concat = np.hstack(image_list)
        
        return image_concat
        
    def cropResizeImage(self, image):
        image_h, image_w = self.image_h, self.image_w
        disp_h = int(image_h * (self.scale*self.width()/image_w)) # Image height displayed on the canvas
        disp_w = int(image_w * (self.scale*self.width()/image_w)) # Image width displayed on the canvas
        
        if disp_w <= image_w:
            img = Image.fromarray(image)
            img = img.resize((disp_w, disp_h), Image.BILINEAR)
            image = np.array(img, dtype=np.uint8)
            
            left = self.left_index
            right = left + self.width()
            if self.top_index > 0: top = self.top_index
            else: top = 0
            bottom = top + self.height()
        else:
            left = int(self.left_index * image_w / disp_w)
            right = int((self.left_index + self.width()) * image_w / disp_w)
            if self.top_index > 0: 
                top = int(self.top_index * image_w / disp_w)
                bottom = int((self.top_index + self.height()) * image_w / disp_w)
            else: 
                top = 0
                bottom = int(self.height() * image_w / disp_w)
            
        image = image[top:bottom, left:right, :]
        
        return image
        
    def convertPixmap(self, image):
        h, w, ch = image.shape[:3]
        bytesPerLine = ch*w
        convertToQtFormat = QImage(image.data.tobytes(), w, h, bytesPerLine, QImage.Format_RGB888)
        self.pixmap = QPixmap.fromImage(convertToQtFormat).scaled(self.size(), Qt.KeepAspectRatio, 
            Qt.SmoothTransformation)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        
        if self.pixmap is not None: 
            off_x = (self.size().width() - self.pixmap.width()) / 2
            off_y = (self.size().height() - self.pixmap.height()) / 2
            painter.drawPixmap(off_x, off_y, self.pixmap)
            
            