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
from PyQt5.QtCore import Qt, QSize, QPoint, QRect, QLineF, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QColor


def format_image(image): # Gray to RGB
    if image is None: return
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
        self.mode = 'live'       # Canvas mode: live or mark
        self.scale = 1.0         # Concatenated image width / widget width, should be larger than 1
        self.is_drag: False      # Whether the drag has been started
        self.is_register = False # Whether the image info has been regisgtered
        self.cursor = QPoint(self.width()/2, self.height()/2) # Cursor position
        self.registerWidget()
        
    def setConfig(self, params):
        self.zoom_factor = params['zoom_factor']
        self.max_scale = params['max_scale']
        self.params = params
        
    def registerWidget(self, logo=None, overview=None):
        self.logo = logo
        self.overview = overview
        
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
    
    def setWidgetGeometry(self):
        image_w = self.image_w
        image_h = self.image_h
        disp_h = image_h * (self.scale*self.width()/image_w) # Image height displayed on the canvas
        disp_w = image_w * (self.scale*self.width()/image_w) # Image width displayed on the canvas
        disp_size = QSize(disp_w, disp_h)
        if self.overview is not None:
            self.overview.refresh(self.size(), disp_size, self.scale, self.left_index, self.top_index)
        
    def mousePressEvent(self, ev):
        if self.mode == 'live':
            self.is_drag = True
            self.cursor = ev.pos()
        elif self.mode == 'mark':
            pass
        
    def mouseMoveEvent(self, ev):
        if self.mode == 'live' and self.is_drag:
            self.moveContent(ev.pos())
            self.setWidgetGeometry()
        elif self.mode == 'mark':
            pass
        
    def mouseReleaseEvent(self, ev):
        self.is_drag = False
        
    def mouseDoubleClickEvent(self, ev):
        if self.scale < self.max_scale:
            self.resizeContent(ev.pos(), op='maximize')
        else:
            self.resizeContent(ev.pos(), op='minimize')
        self.setWidgetGeometry()
        
    def wheelEvent(self, ev):
        angle = ev.angleDelta().y()
        position = ev.pos()
        self.resizeContent(position, angle)
        self.setWidgetGeometry()
        
    def moveContent(self, position):
        x0, y0 = self.cursor.x(), self.cursor.y()
        x, y = position.x(), position.y()
        
        image_h, image_w = self.image_h, self.image_w        # Original image height and width
        disp_h = image_h * (self.scale*self.width()/image_w) # Image height displayed on the canvas
        disp_w = image_w * (self.scale*self.width()/image_w) # Image width displayed on the canvas
        
        # Update the over-widget pixels
        off_x = x - x0
        off_y = y - y0
        self.left_index = max(0, self.left_index - off_x)
        self.left_index = min(int(disp_w-self.width()), self.left_index)
        if disp_h > self.height():#self.top_index >= 0: 
            self.top_index = max(0, self.top_index - off_y)
            self.top_index = min(int(disp_h-self.height()), self.top_index)
        
        self.cursor = position
        
    def resizeContent(self, position, angle=0, op='normal'):
        x, y = position.x(), position.y()
        
        # Update the scale and scale factor
        if op in ['maximize', 'minimize']: 
            if self.top_index < 0 and (y<=abs(self.top_index) \
                or y>=abs(self.height()-abs(self.top_index))):
                return
            if op == 'maximize': 
                scale = self.max_scale
            elif op == 'minimize': 
                self.resetContent()
                return
            
        elif angle > 0: scale = min(self.max_scale, self.scale*self.zoom_factor)
        else: scale = max(1.0, self.scale/self.zoom_factor)
        scale_factor = scale / self.scale
        
        image_h, image_w = self.image_h, self.image_w   # Image height and width
        disp_h = image_h * (scale*self.width()/image_w) # Image height displayed on the canvas
        disp_w = image_w * (scale*self.width()/image_w) # Image width displayed on the canvas
        
        # Distance from the cursor to the displayed image's boundary after resize
        left_image_len = int((x + self.left_index) * scale_factor)
        self.left_index = max(0, left_image_len - x)
        
        if disp_h < self.height():
            self.top_index = int((disp_h - self.height())/2)
        else:
            if self.top_index >= 0:
                top_image_len = (y + self.top_index) * scale_factor
                self.top_index = int(top_image_len - y)
            else:
                abs_top_index = abs(self.top_index)
                if y < abs_top_index: y = abs_top_index + 1
                elif y > self.height() - abs_top_index: y = self.height() - abs_top_index - 1
                
                dist_to_image_top = y - abs_top_index
                if dist_to_image_top * scale_factor < y:
                    self.top_index = 0
                else:
                    self.top_index = min(disp_h-self.height(), dist_to_image_top*scale_factor-y)
        
        self.scale = scale
        
    def resetContent(self):
        self.left_index = 0
        self.top_index = int((self.height() - self.width()/self.image_w*self.image_h) / 2) * -1
        self.scale = 1.0
        
    def registerImageInfo(self, image):
        assert self.scale == 1.0, 'Initial scale should be 1.0'
        self.image_h, self.image_w = image.shape[:2]
        widget_h, widget_w = self.height(), self.width()
        
        self.resetContent()
        self.setWidgetGeometry()
        self.is_register = True
     
    def concatImageList(self, image_list):
        image_list = self.checkImageList(image_list)
        if len(image_list) == 0: return None
        elif len(image_list) == 1: return image_list[0]
        
        image_list = tuple(image_list)
        image_concat = np.hstack(image_list)
        
        return image_concat
        
    def checkImageList(self, image_list):
        image_list_checked = list()
        for i, image in enumerate(image_list):
            if image is None: continue
            image = format_image(image)
            image_list_checked.append(image)
        
        return image_list_checked
        
    def cropResizeImage(self, image):
        image_h, image_w = self.image_h, self.image_w
        disp_h = int(image_h * (self.scale*self.width()/image_w)) # Image height displayed on the canvas
        disp_w = int(image_w * (self.scale*self.width()/image_w)) # Image width displayed on the canvas
        
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
            off_x = (self.width() - self.pixmap.width()) / 2
            off_y = (self.height() - self.pixmap.height()) / 2
            painter.drawPixmap(off_x, off_y, self.pixmap)
            
            