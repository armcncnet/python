"""
******************************************************************************
* @author  ARMCNC site:www.armcnc.net github:armcnc.github.io
******************************************************************************
"""

import linuxcnc
from .status import Statistics
from .command import Command
from .error import Error

class CNC:

    def __init__(self, framework):
        self.framework = framework
        self.linuxcnc = linuxcnc
        self.statistics = Statistics()
        self.command = Command()
        self.error = Error()

    def get_npts(self, arg):
        pass

    def start(self, arg):
        self.linuxcnc.start(arg)

    def clear(self):
        self.linuxcnc.clear()

    def stop(self):
        self.linuxcnc.stop()

    def call(self):
        self.linuxcnc.call()

    def last(self, line):
        self.linuxcnc.last(line)
