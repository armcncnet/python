#!/usr/bin/env python
# -*- coding: utf-8 -*-

import armcnc.drives.gpio as drives

def on_start(drive):
    drive.base.setup()
    while True:
        drive.base.loop()

if __name__ == '__main__':
    drives.Init()
