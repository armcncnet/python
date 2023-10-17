"""
******************************************************************************
* @author  ARMCNC site:www.armcnc.net github:armcnc.github.io
******************************************************************************
"""

import sys
import subprocess
from .status import Status
from .command import Command
from .ini_file import INIFile
from .error_channel import ErrorChannel

class CNC:

    def __init__(self, framework):
        self.framework = framework
        self.status = Status(self.framework)
        self.command = Command(self.framework)
        self.ini_file = INIFile(self.framework)
        self.error_channel = ErrorChannel(self.framework)

    def start(self):
        linuxcnc_pid = subprocess.Popen(["pidof", "-x", "linuxcnc"], stdout=subprocess.PIPE)
        linuxcnc_pid_result = linuxcnc_pid.communicate()[0]
        if len(linuxcnc_pid_result) == 0:
            linuxcnc_start = "sudo -u " + self.framework.machine.user + " linuxcnc" + sys.argv[1]
            subprocess.Popen(linuxcnc_start, stderr=subprocess.STDOUT, shell=True)

