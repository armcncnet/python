#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .armcnc import Init

# armcnc启动回调函数
def armcnc_start(cnc):
    while True:
        pass

def armcnc_message(cnc, message):
    pass

def armcnc_exit(cnc):
    pass

if __name__ == '__main__':
    Init()
