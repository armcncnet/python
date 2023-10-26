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
            self.set_teleop_enable_mode(teleop_mode)
        return mode

    def home_axis(self, axis):
        self.api.set_mode(linuxcnc.MODE_MANUAL, 1)
        self.api.api.home(axis)
        self.api.api.wait_complete()

    def all_homed(self):
        homed = True
        self.father.status.api.poll()
        for i, h in enumerate(self.father.status.api.homed):
            if i >= len(self.father.machine.coordinates):
                break
            homed = homed and h
        return homed


