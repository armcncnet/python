"""
******************************************************************************
* @author  ARMCNC site:www.armcnc.net github:armcnc.github.io
******************************************************************************
"""

import sys
import subprocess
from .status import Status
from .command import Command
from .ini import Ini
from .error import Error

class CNC:

    def __init__(self, framework):
        self.framework = framework
        self.status = None
        self.command = None
        self.ini = None
        self.error = None

    def start(self):
        linuxcnc_pid = subprocess.Popen(["pidof", "-x", "linuxcnc"], stdout=subprocess.PIPE)
        linuxcnc_pid_result = linuxcnc_pid.communicate()[0]
        if len(linuxcnc_pid_result) == 0:
            linuxcnc_start = "sudo -u " + self.framework.machine.user + " linuxcnc" + sys.argv[1]
            subprocess.Popen(linuxcnc_start, stderr=subprocess.STDOUT, shell=True)

        self.status = Status(self.framework)
        self.command = Command(self.framework)
        self.ini = Ini(self.framework)
        self.error = Error(self.framework)
