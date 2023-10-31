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
        self.task = threading.Thread(name="status_task", target=self.task_work)
        self.task.daemon = True
        self.task.start()

    def task_work(self):
        while True:
            if self.father.framework.machine.is_alive and self.father.framework.utils.service.status:
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
                    self.father.framework.machine.machine_path = self.father.framework.machine.info["ini_filename"].replace(self.father.framework.machine.workspace+"/configs/", "").replace("/machine.ini", "")
                    user_data = {
                        "user": self.father.framework.machine.user,
                        "workspace": self.father.framework.machine.workspace,
                        "machine_path": self.father.framework.machine.machine_path,
                        "control": int(self.father.framework.machine.get_user_config_value("BASE", "CONTROL") or 0),
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
                        "homed": self.father.framework.machine.info["homed"],
                        "spindle": {
                            "enabled": self.father.framework.machine.info["spindle"][0]["enabled"],
                            "direction": self.father.framework.machine.info["spindle"][0]["direction"],
                            "speed": self.father.framework.machine.info["spindle"][0]["speed"],
                            "max_speed": int(self.father.framework.machine.get_user_config_value("SPINDLE", "MAX_SPEED") or 24000),
                            "default_speed": int(inifile.find("DISPLAY", "DEFAULT_SPINDLE_SPEED")),
                            "min_override": float(inifile.find("DISPLAY", "MIN_SPINDLE_OVERRIDE")),
                            "max_override": float(inifile.find("DISPLAY", "MAX_SPINDLE_OVERRIDE")),
                            "override": self.father.framework.machine.info["spindle"][0]["override"],
                            "override_enabled": self.father.framework.machine.info["spindle"][0]["override_enabled"]
                        },
                        "feed": {
                            "max_override": float(inifile.find("DISPLAY", "MAX_FEED_OVERRIDE")),
                            "rate": float(self.father.framework.machine.info["feedrate"])
                        },
                        "ext_info": self.father.framework.machine.get_user_config_items("EXTINFO"),
                        "max_linear_velocity": float(inifile.find("DISPLAY", "MAX_LINEAR_VELOCITY")),
                        "max_velocity": float(self.father.framework.machine.info["max_velocity"]),
                        "default_linear_velocity": float(inifile.find("DISPLAY", "DEFAULT_LINEAR_VELOCITY")),
                        "max_angular_velocity": float(inifile.find("DISPLAY", "MAX_ANGULAR_VELOCITY")),
                        "default_angular_velocity": float(inifile.find("DISPLAY", "DEFAULT_ANGULAR_VELOCITY"))
                    }

                    self.father.framework.machine.info["user_data"] = user_data

                    self.father.framework.machine.axis = user_data["coordinates"]

                    if user_data["task_state"] == 4:
                        self.father.framework.machine.task_state = True
                    else:
                        self.father.framework.machine.task_state = False

                    self.father.framework.utils.service.service_write({"command": "launch:machine:info", "message": "", "data": self.father.framework.machine.info})
            self.father.framework.utils.set_sleep(0.05)

