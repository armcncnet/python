"""
******************************************************************************
* @author  ARMCNC site:www.armcnc.net github:armcnc.github.io
******************************************************************************
"""

import sys
import subprocess
import linuxcnc
from .status import Status
from .command import Command
from .ini import Ini
from .error import Error

class CNC:

    def __init__(self, framework):
        self.framework = framework
        self.status = Status(self.framework)
        self.command = Command(self.framework)
        self.ini = Ini(self.framework)
        self.error = Error(self.framework)

    def start(self):
        linuxcnc_pid = subprocess.Popen(["pidof", "-x", "linuxcnc"], stdout=subprocess.PIPE)
        linuxcnc_pid_result = linuxcnc_pid.communicate()[0]
        if len(linuxcnc_pid_result) == 0:
            linuxcnc_start = "sudo -u " + self.framework.machine.user + " " + self.framework.machine.display + " " + "linuxcnc " + sys.argv[1]
            subprocess.Popen(linuxcnc_start, stderr=subprocess.STDOUT, shell=True)
        # self.framework.machine.is_alive = True

    def message_callback(self, message):
        if message and message["command"] and message["command"] != "":
            if message["command"] == "desktop:control:device:estop":
                self.status.api.poll()
                if self.status.api.task_state == linuxcnc.STATE_ESTOP:
                    self.command.api.state(linuxcnc.STATE_ESTOP_RESET)
                else:
                    if self.status.api.task_state == linuxcnc.STATE_ESTOP_RESET or self.status.api.task_state == linuxcnc.STATE_ON or self.status.api.task_state == linuxcnc.STATE_OFF:
                        self.command.api.state(linuxcnc.STATE_ESTOP)
                self.command.api.wait_complete(0.5)

            if message["command"] == "desktop:control:device:start":
                self.status.api.poll()
                if self.status.api.task_state == linuxcnc.STATE_ESTOP:
                    return False
                if self.status.api.task_state == linuxcnc.STATE_ON:
                    self.command.api.state(linuxcnc.STATE_OFF)
                else:
                    if self.status.api.task_state == linuxcnc.STATE_OFF or self.status.api.task_state == linuxcnc.STATE_ESTOP_RESET:
                        self.command.api.state(linuxcnc.STATE_ON)
                self.command.api.wait_complete(0.5)

                print("read_line", self.status.api.read_line)
                print("linear_units", self.status.api.linear_units)
                print("paused", self.status.api.paused)
                print("estop", self.status.api.estop)
                print("enabled", self.status.api.enabled)
                print("state", self.status.api.state)
                print("interp_state", self.status.api.interp_state)
                print("task_state", self.status.api.task_state)
                print("homed", self.status.api.homed)
                print("--------------------")



