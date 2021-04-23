#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 04.23.2021
Updated on 04.23.2021

Author: haoshuai@handaotech.com
'''

import os
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot


class MarkWidget(QDialog):
    markSignal = pyqtSignal(str)
    saveSignal = pyqtSignal(dict)
    
    def __init__(self, parent=None):
        super(MarkWidget, self).__init__(parent)
        loadUi(os.path.join(os.path.abspath(os.path.dirname(__file__)), "MarkWidget.ui"), self)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowFlags(Qt.Widget)
        self.initParams()
        
    def initParams(self):
        self.exclusive_dict = {
            'point': self.btnPoint,
            'line': self.btnLine,
            'circle': self.btnCircle,
            'rect': self.btnRect
        }
        
    @pyqtSlot()
    def setPointMarker(self):
        self.setBtnExclusive('point')
        
    @pyqtSlot()
    def setLineMarker(self):
        self.setBtnExclusive('line')
        
    @pyqtSlot()
    def setCircleMarker(self):
        self.setBtnExclusive('circle')
        
    @pyqtSlot()
    def setRectMarker(self):
        self.setBtnExclusive('rect')
        
    @pyqtSlot()
    def save(self):
        pass
        
    @pyqtSlot()
    def undo(self):
        pass
        
    @pyqtSlot()
    def discard(self):
        pass
        
    def setBtnExclusive(self, name):
        for btn_name in self.exclusive_dict:
            if btn_name != name:
                btn = self.exclusive_dict[btn_name]
                btn.resetButton()