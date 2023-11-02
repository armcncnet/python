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
        self.status = Status(self)
        self.command = Command(self)
        self.error = Error(self)

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
                self.command.override_limits()

            if message["command"] == "desktop:control:device:home":
                if len(self.framework.machine.axes) > 0:
                    if message["data"] == "all":
                        self.command.home_all()
                    else:
                        value = int(message["data"])
                        self.command.home_axis(value)

            if message["command"] == "desktop:control:relative:offset":
                if len(self.framework.machine.axes) > 0:
                    if message["data"]["id"] == "all":
                        self.command.set_axis_offset_all(message["data"])
                    else:
                        self.command.set_axis_offset(message["data"])

            if message["command"] == "desktop:control:jog:start":
                axis = message["data"]["axis"]
                speed = message["data"]["speed"]
                jog_mode = self.command.get_jog_mode()
                if jog_mode:
                    axis = self.framework.machine.get_axes_num(axis)
                else:
                    axis = self.framework.machine.get_axis_num(axis)
                speed = speed / 60
                increment = message["data"]["increment"]
                if increment == -1:
                    self.command.jog_continuous(axis, speed, jog_mode)
                else:
                    self.command.jog_increment(axis, speed, increment, jog_mode)

            if message["command"] == "desktop:control:jog:stop":
                axis = message["data"]["axis"]
                jog_mode = self.command.get_jog_mode()
                if jog_mode:
                    axis = self.framework.machine.get_axes_num(axis)
                else:
                    axis = self.framework.machine.get_axis_num(axis)
                self.command.jog_stop(axis, jog_mode)

            if message["command"] == "desktop:control:spindle":
                value = message["data"]["value"]
                self.command.set_spindle(value)

            if message["command"] == "desktop:control:spindle:override":
                value = message["data"]["value"]
                self.command.set_spindle_override(value)

            if message["command"] == "desktop:control:max:velocity":
                value = message["data"]["value"]
                self.command.set_max_velocity(value)

            if message["command"] == "desktop:control:feed:rate":
                value = message["data"]["value"]
                self.command.set_feed_rate(value)

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
