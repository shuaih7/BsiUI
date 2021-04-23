#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 04.23.2021
Updated on 04.23.2021

Author: haoshuai@handaotech.com
'''

import os
from PyQt5.QtWidgets import QMessageBox


class MessageBox(QMessageBox):
    def __init__(self, parent=None):
        super(MessageBox, self).__init__(parent)
        self.setStyleSheet('background-color:rgb(180,180,180)')
        
    def show(self):
        super(MessageBox, self).show(parent)