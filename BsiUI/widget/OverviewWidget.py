#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 04.20.2021
Updated on 04.20.2021

Author: haoshuai@handaotech.com
'''

import os
from PyQt5.QtWidgets import QLabel


class OverviewWidget(QLabel):
    def __init__(self, parent=None):
        super(OverviewWidget, self).__init__(parent)
        
    def setConfig(self, params):
        self.params = params
        
    def resizeWidget(self, size):
        pass