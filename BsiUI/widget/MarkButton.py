#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 04.23.2021
Updated on 04.23.2021

Author: haoshuai@handaotech.com
'''

import os
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QPushButton


class MarkButton(QPushButton):
    
    def __init__(self, parent=None):
        super(MarkButton, self).__init__(parent)
        self.main_style = "border-radius:8px;padding:2px 4px;"
        self.color = "background-color:rgba(180,180,180,0%)"
        self.press_color = "background-color:rgba(180,180,180,75%)"
        self.is_pressed = False
        
    def setConfig(self, params):
        self.params = params
        
    def resizeWidget(self, size):
        off_w = self.params['off_w']
        ratio_top = self.params['ratio_top']
        ratio_right = self.params['ratio_right']
        ratio_w = self.params['ratio_w']
        ratio_h = self.params['ratio_h']
        
        frame_h, frame_w = size.height(), size.width()
        x = int((1-ratio_right)*frame_w) + off_w
        y = int(ratio_top*frame_h)
        h = int(ratio_h * frame_h)
        w = h #int(ratio_w * frame_w)
        self.setGeometry(x, y, w, h)
        self.setIconSize(QSize(int(w*0.8), int(h*0.8)))

    def mousePressEvent(self, event):
        super(MarkButton, self).mousePressEvent(event)
        if not self.is_pressed:
            self.setStyleSheet(self.main_style+self.press_color)
            self.is_pressed = True
        else:
            self.setStyleSheet(self.main_style+self.color)
            self.is_pressed = False