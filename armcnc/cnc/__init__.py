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
from .error import Error

class CNC:

    def __init__(self, framework):
        self.framework = framework
        self.status = Status(self.framework)
        self.command = Command(self.framework)
        self.error = Error(self.framework)

    def start(self):
        linuxcnc_pid = subprocess.Popen(["pidof", "-x", "linuxcnc"], stdout=subprocess.PIPE)
        linuxcnc_pid_result = linuxcnc_pid.communicate()[0]
        if len(linuxcnc_pid_result) == 0:
            self.framework.utils.service.service_write({"command": "launch:restart", "message": "", "data": False})
            sys.exit()
        self.framework.machine.is_alive = True
        self.framework.utils.service.service_write({"command": "launch:restart", "message": "", "data": True})

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

            if message["command"] == "desktop:control:device:override_limits":
                self.command.set_mode(linuxcnc.MODE_MANUAL, 0.5)
                self.command.api.override_limits()
                self.command.api.wait_complete(0.5)

            if message["command"] == "desktop:control:device:home":
                if len(self.framework.machine.coordinates) > 0:
                    self.command.set_teleop_enable(0)
                    if message["data"] == "all":
                        # 优先Z轴回零
                        self.command.home_axis(2)
                        for x in range(len(self.framework.machine.coordinates) - 1, -1, -1):
                            if x == 2:
                                continue
                            self.command.home_axis(x)
                    else:
                        value = int(message["data"])
                        self.command.set_teleop_enable_mode(0)
                        self.command.home_axis(value)

            if message["command"] == "desktop:control:jog:start":
                pass

            if message["command"] == "desktop:control:jog:stop":
                pass

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
