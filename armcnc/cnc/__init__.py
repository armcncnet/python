"""
******************************************************************************
* @author  ARMCNC site:www.armcnc.net github:armcnc.github.io
******************************************************************************
"""

from .status import Status
from .command import Command
from .ini_file import IniFile
from .position_logger import PositionLogger
from .error_channel import ErrorChannel

class CNC:

    def __init__(self, framework):
        self.framework = framework
        self.stat = Status()
        self.command = Command()
        self.ini_file = IniFile()
        self.position_logger = PositionLogger()
        self.error_channel = ErrorChannel()
