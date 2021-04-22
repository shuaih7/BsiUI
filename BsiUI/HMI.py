#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Created on 04.11.2021
Updated on 04.19.2021

Author: haoshuai@handaotech.com
"""

import os
import sys
import cv2
import json
import time

abs_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(abs_path)

from PyQt5.uic import loadUi
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot, QEvent, QSize, QRegExp
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QMessageBox

from device import OpenCVCamera


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        loadUi(os.path.join(os.path.abspath(os.path.dirname(__file__)), "HMI.ui"), self)
        
        self.loadConfigMatrix()
        self.initWidgets()
        self.initParmas()
        self.initCamera()
        
    def loadConfigMatrix(self):
        config_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), "config.json")
        with open (config_file, "r") as f: 
            self.config_matrix = json.load(f)
            f.close()
            
    def initWidgets(self):
        widget_params = self.config_matrix['Widget']
        self.canvas.setConfig(widget_params['Canvas'])
        self.lbLogo.setConfig(widget_params['LogoWidget'])
        self.lbOverview.setConfig(widget_params['OverviewWidget'])
        
        self.frame_resize_list = [
            self.canvas,
            self.lbLogo,
            self.lbOverview
        ]
        
    def initParmas(self):
        self.is_live = True
        
    def initCamera(self):
        camera_params = self.config_matrix['Camera']
        self.camera = OpenCVCamera(camera_params)
        
    def resizeEvent(self, ev):
        self.resizeFrameWidget()
    
    def resizeFrameWidget(self):
        for widget in self.frame_resize_list:
            widget.resizeWidget(self.frame.size())
            
    def live(self):
        self.resizeFrameWidget()
        
        while self.is_live:
            image_list = self.camera.getImageList()
            self.canvas.refresh(image_list)
            QApplication.processEvents()
            
    def closeEvent(self, ev):   
        reply = QMessageBox.question(
            self,
            "退出程序",
            "您确定要退出吗?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No)

        if reply == QMessageBox.Yes: 
            #self.messager("FabricUI 已关闭。\n", flag="info")
            sys.exit()
        else: ev.ignore()
        
        
        
        
        