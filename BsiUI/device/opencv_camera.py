#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 04.20.2021
Updated on 04.20.2021

Author: haoshuai@handaotech.com
'''

import os
import cv2
import numpy as np
from .camera import Camera


class OpenCVCamera(Camera):
    def __init__(self, params):
        self.updateParams(params)
        
    def updateParams(self, params):
        self.params = params
        self.initSettings()

    def initSettings(self):
        self.camera_num = self.params['camera_num']
        #self.set_expo(self.params["exposure_time"])
        #self.set_gain(self.params["gain"])
        #self.set_binning(self.params["binning"])
        
        self.image = cv2.imread(r'C:\Users\shuai\Documents\GitHub\BsiUI\develop\GE90_1.png', -1)
        self.image_list = [self.image, self.image, self.image, self.image]
        
    def connect(self):
        pass
        
    def reconnect(self):
        pass
        
    def getImage(self):
        return self.image
        
    def getImageList(self):
        return self.image_list
        