"""
******************************************************************************
* @author  ARMCNC site:www.armcnc.net github:armcnc.github.io
******************************************************************************
"""

import threading
import linuxcnc


class Status:

    def __init__(self, father):
        self.father = father
        self.linuxcnc = linuxcnc
        self.api = linuxcnc.stat()
        self.task = threading.Thread(name="status_task", target=self.task)
        self.task.daemon = True
        self.task.start()

    def task(self):
        while True:
            if self.father.framework.machine.is_alive:
                try:
                    self.api.poll()
                except linuxcnc.error as detail:
                    self.father.framework.utils.service.service_write(
                        {"command": "launch:machine:error", "message": detail, "data": False})

                self.father.framework.machine.info = {}
                for x in dir(self.api):
                    if not x.startswith("_") and not callable(getattr(self.api, x)):
                        self.father.framework.machine.info[x] = getattr(self.api, x)

                if self.father.framework.machine.info["ini_filename"]:
                    inifile = linuxcnc.ini(self.father.framework.machine.info["ini_filename"])
                    user_data = {
                        "user": self.father.framework.machine.user,
                        "increments": [value.replace("mm", "") for value in inifile.find("DISPLAY", "INCREMENTS").split(",")],
                        "coordinates": list(inifile.find("TRAJ", "COORDINATES")) or [],
                        "linear_units": inifile.find("TRAJ", "LINEAR_UNITS") or "mm",
                        "angular_units": inifile.find("TRAJ", "ANGULAR_UNITS") or "degree",
                        "estop": self.father.framework.machine.info["estop"],
                        "paused": self.father.framework.machine.info["paused"],
                        "enabled": self.father.framework.machine.info["enabled"],
                        "state": self.father.framework.machine.info["state"],
                        "interp_state": self.father.framework.machine.info["interp_state"],
                        "task_state": self.father.framework.machine.info["task_state"],
                        "homed": self.father.framework.machine.info["homed"]
                    }

                    self.father.framework.machine.info["user_data"] = user_data

                    self.father.framework.machine.axis = user_data["coordinates"]

                    self.father.framework.utils.service.service_write({"command": "launch:machine:info", "message": "", "data": self.father.framework.machine.info})
            self.father.framework.utils.set_sleep(0.05)

