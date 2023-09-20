"""
******************************************************************************
* @author  ARMCNC site:www.armcnc.net github:armcnc.github.io
******************************************************************************
"""

from .status import Status
from .command import Command
from .logger import Logger
from .error import Error

class CNC:

    def __init__(self, framework):
        self.framework = framework
        self.stat = Status()
        self.command = Command()
        self.logger = Logger()
        self.error = Error()
