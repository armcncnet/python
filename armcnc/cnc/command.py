"""
******************************************************************************
* @author  ARMCNC site:www.armcnc.net github:armcnc.github.io
******************************************************************************
"""

import linuxcnc

class Command:

    def __init__(self, father):
        self.father = father
        self.linuxcnc = linuxcnc
        self.api = self.linuxcnc.command()

    def set_mode(self, m, t, *p):
        self.father.status.api.poll()
        if self.father.status.api.task_mode == m or self.father.status.api.task_mode in p:
            return True
        self.api.mode(m)
        if t == 0:
            self.api.wait_complete()
        else:
            self.api.wait_complete(t)
        self.father.status.api.poll()
        return True

    def set_teleop_enable(self, value):
        self.father.status.api.poll()
        self.api.teleop_enable(value)
        self.api.wait_complete()

    def set_teleop_enable_mode(self, value):
        self.father.status.api.poll()
        if self.father.status.api.task_mode != linuxcnc.MODE_MANUAL:
            self.set_mode(linuxcnc.MODE_MANUAL, 1)
        if self.get_jog_mode():
            return
        self.api.teleop_enable(value)
        self.api.wait_complete(0.1)
        self.father.status.api.poll()
        return True

    def get_jog_mode(self):
        self.father.status.api.poll()
        if self.father.status.api.kinematics_type == linuxcnc.KINEMATICS_IDENTITY and self.all_homed():
            teleop_mode = 1
            mode = False
        elif self.father.status.api.motion_mode == linuxcnc.TRAJ_MODE_FREE:
            teleop_mode = 0
            mode = True
        else:
            teleop_mode = 1
            mode = False
        if mode and self.father.status.api.motion_mode != linuxcnc.TRAJ_MODE_FREE or not mode and self.father.status.api.motion_mode != linuxcnc.TRAJ_MODE_TELEOP:
            self.set_teleop_enable(teleop_mode)
        return mode

    def jog_continuous(self, axis, speed, mode):
        if mode == "":
            mode = self.get_jog_mode()
        self.set_mode(linuxcnc.MODE_MANUAL, 0.5)
        self.api.jog(linuxcnc.JOG_CONTINUOUS, mode, int(axis), int(speed))

    def jog_increment(self, axis, speed, increment, mode):
        if mode == "":
            mode = self.get_jog_mode()
        increment = float(increment)
        self.set_mode(linuxcnc.MODE_MANUAL, 0.5)
        self.api.jog(linuxcnc.JOG_INCREMENT, mode, int(axis), int(speed), increment)

    def jog_stop(self, axis, mode):
        if mode == "":
            mode = self.get_jog_mode()
        self.api.jog(linuxcnc.JOG_STOP, mode, int(axis))

    def home_axis(self, axis):
        self.set_mode(linuxcnc.MODE_MANUAL, 1)
        self.api.home(axis)
        self.api.wait_complete()

    def all_homed(self):
        homed = True
        self.father.status.api.poll()
        for i, h in enumerate(self.father.status.api.homed):
            if i >= len(self.father.framework.machine.axis):
                break
            homed = homed and h
        return homed


