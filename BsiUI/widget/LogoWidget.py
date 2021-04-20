#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 04.20.2021
Updated on 04.20.2021

Author: haoshuai@handaotech.com
'''

import os
from PyQt5.QtWidgets import QLabel


class LogoWidget(QLabel):
    def __init__(self, parent=None):
        super(LogoWidget, self).__init__(parent)
        
    def setConfig(self, params):
        self.params = params
        
    def resizeWidget(self, size):
        off_w = int(self.params['off_w'])
        off_h = int(self.params['off_h'])
        ratio_w = float(self.params['ratio_w'])
        ratio_h = float(self.params['ratio_h'])
        
        width = int(size.width() * ratio_w)
        height = int(size.height() * ratio_h)
        self.setGeometry(off_w, off_h, width, height)