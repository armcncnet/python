"""
******************************************************************************
* @author  ARMCNC site:www.armcnc.net github:armcnc.github.io
******************************************************************************
"""

import linuxcnc

class Logger:

    def __init__(self):
        self.linuxcnc = linuxcnc
        self.api = self.linuxcnc.positionlogger()

    def get_npts(self):
        return self.api.npts

    def start(self, arg):
        self.api.start(arg)

    def clear(self):
        self.api.clear()

    def stop(self):
        self.api.stop()

    def call(self):
        self.api.call()

    def last(self, line):
        self.api.last(line)
