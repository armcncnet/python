"""
******************************************************************************
* @author  ARMCNC site:www.armcnc.net github:armcnc.github.io
******************************************************************************
"""

import threading
import linuxcnc


class Status:

    def __init__(self, framework):
        self.framework = framework.framework
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

                self.framework.machine.info = {}
                for x in dir(self.api):
                    if not x.startswith("_") and not callable(getattr(self.api, x)):
                        self.framework.machine.info[x] = getattr(self.api, x)

                if self.framework.machine.info["ini_filename"]:
                    inifile = linuxcnc.ini(self.framework.machine.info["ini_filename"])
                    user_data = {
                        "user": self.framework.machine.user,
                        "increments": list(inifile.find("DISPLAY", "INCREMENTS")) or [],
                        "coordinates": list(inifile.find("TRAJ", "COORDINATES")) or [],
                        "linear_units": inifile.find("TRAJ", "LINEAR_UNITS") or "mm",
                        "angular_units": inifile.find("TRAJ", "ANGULAR_UNITS") or "degree",
                        "estop": self.framework.machine.info["estop"],
                        "paused": self.framework.machine.info["paused"],
                        "enabled": self.framework.machine.info["enabled"],
                        "state": self.framework.machine.info["state"],
                        "interp_state": self.framework.machine.info["interp_state"],
                        "task_state": self.framework.machine.info["task_state"],
                        "homed": self.framework.machine.info["homed"]
                    }
                    self.framework.machine.info["user_data"] = user_data

                    self.framework.machine.axis = user_data["coordinates"]

                    self.framework.utils.service.service_write({"command": "launch:machine:info", "message": "", "data": self.framework.machine.info})
            self.framework.utils.set_sleep(0.05)

