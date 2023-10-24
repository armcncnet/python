"""
******************************************************************************
* @author  ARMCNC site:www.armcnc.net github:armcnc.github.io
******************************************************************************
"""

import threading
import linuxcnc


class Status:

    def __init__(self, framework):
        self.framework = framework
        self.linuxcnc = linuxcnc
        self.api = linuxcnc.stat()
        self.task = threading.Thread(name="status_task", target=self.task)
        self.task.daemon = True
        self.task.start()

    def task(self):
        while True:
            if self.framework.machine.is_alive:
                try:
                    self.api.poll()
                except linuxcnc.error as detail:
                    self.framework.utils.service.service_write(
                        {"command": "launch:machine:error", "message": detail, "data": False})

                self.framework.machine.stat = {}
                for x in dir(self.api):
                    if not x.startswith("_") and not callable(getattr(self.api, x)):
                        self.framework.machine.stat[x] = getattr(self.api, x)

                inifile = linuxcnc.ini(self.framework.machine.stat["ini_filename"])
                user_data = {
                    "status": self.framework.machine.stat,
                    "user": self.framework.machine.user,
                    "increments": inifile.find("DISPLAY", "INCREMENTS") or [],
                    "coordinates": inifile.find("TRAJ", "COORDINATES") or "unknown",
                    "linear_units": inifile.find("TRAJ", "LINEAR_UNITS") or "mm",
                    "angular_units": inifile.find("TRAJ", "ANGULAR_UNITS") or "degree",
                }

                self.framework.utils.service.service_write({"command": "launch:machine:status", "message": "", "data": user_data})
            self.framework.utils.set_sleep(0.05)
