#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 04.11.2021
Updated on 04.11.2021

Author: haoshuai@handaotech.com
'''

import sys
from PyQt5.QtWidgets import QApplication
app = QApplication(sys.argv)
from HMI import MainWindow


def main():
    Window = MainWindow()
    #Window.showMaximized()
    Window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()