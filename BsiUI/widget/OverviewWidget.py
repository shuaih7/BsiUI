#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 04.20.2021
Updated on 04.23.2021

Author: haoshuai@handaotech.com
'''

import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QLabel


class OverviewWidget(QLabel):
    def __init__(self, parent=None):
        super(OverviewWidget, self).__init__(parent)
        self.initParams()
        
    def initParams(self):
        self.color = QColor(255,165,0)
        self.ov_left = 0
        self.ov_right = 0
        self.ov_top = 0
        self.ov_bottom = 0
        
    def setConfig(self, params):
        self.params = params
        
    def resizeWidget(self, size):
        ratio_top = self.params['ratio_top']
        ratio_right = self.params['ratio_right']
        ratio_w = self.params['ratio_w']
        ratio_h = self.params['ratio_h']
        
        frame_h, frame_w = size.height(), size.width()
        x = int((1-ratio_w-ratio_right)*frame_w)
        y = int(ratio_top*frame_h)
        w = int(ratio_w * frame_w)
        h = int(ratio_h * frame_h)
        self.setGeometry(x, y, w, h)
        
    def refresh(self, size, disp_size, scale, left_index, top_index):
        frame_h, frame_w = size.height(), size.width()
        disp_h, disp_w = disp_size.height(), disp_size.width()
        ov_height, ov_width = self.height(), self.width()
        
        self.ov_left = int(left_index/(frame_w*scale)*ov_width)
        self.ov_right = int((left_index+frame_w)/disp_w*ov_width)
        if top_index <= 0:
            self.ov_top = 0
            self.ov_bottom = ov_height
        else:
            self.ov_top = int(top_index/(frame_h*scale)*ov_height)
            self.ov_bottom = int((top_index+frame_h)/disp_h*ov_height)
            
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        rect_h = self.ov_bottom - self.ov_top
        rect_w = self.ov_right - self.ov_left
        
        painter.setBrush(self.color)
        painter.drawRect(self.ov_left, self.ov_top, rect_w, rect_h)