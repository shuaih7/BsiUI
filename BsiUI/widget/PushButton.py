#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 04.23.2021
Updated on 04.23.2021

Author: haoshuai@handaotech.com
'''

import os
from PyQt5.QtWidgets import QPushButton


class PushButton(QPushButton):
    
    def __init__(self, parent=None):
        super(PushButton, self).__init__(parent)
        self.main_style = "border:2px groove gray; border-radius:8px;padding:2px 4px;"
        self.color = "background-color:rgb(160,160,160)"
        self.press_color = "background-color: rgb(125,125,125)"
        
        self.btnHoldList = ["btnPoint", "btnLine", 'btnCircle', 'btnRect']

    def mousePressEvent(self, event):
        super(PushButton, self).mousePressEvent(event)
        self.setStyleSheet(self.main_style+self.press_color)

    def mouseReleaseEvent(self, event):
        super(PushButton, self).mouseReleaseEvent(event)
        if self.objectName() not in self.btnHoldList:
            self.setStyleSheet(self.main_style+self.color)
            
    def resetButton(self):
        self.setStyleSheet(self.main_style+self.color)
        

            