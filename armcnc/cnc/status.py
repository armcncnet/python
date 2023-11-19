"""
******************************************************************************
* @author  ARMCNC site:www.armcnc.net github:armcnc.github.io
******************************************************************************
"""
import copy
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
                    self.father.framework.utils.service.service_write({"command": "launch:machine:error", "message": detail, "data": False})

                self.father.framework.machine.info = {}

                for x in dir(self.api):
                    if not x.startswith("_") and not callable(getattr(self.api, x)):
                        self.father.framework.machine.info[x] = getattr(self.api, x)

                if self.father.framework.machine.info["ini_filename"]:
                    inifile = linuxcnc.ini(self.father.framework.machine.info["ini_filename"])
                    user_data = {
                        "user": self.father.framework.machine.user,
                        "workspace": self.father.framework.machine.workspace,
                        "machine_path": self.father.framework.machine.machine_path,
                        "control": int(self.father.framework.machine.get_user_config_value("BASE", "CONTROL") or 0),
                        "increments": [value.replace("mm", "") for value in inifile.find("DISPLAY", "INCREMENTS").split(",")],
                        "axes": list(inifile.find("TRAJ", "COORDINATES")) or [],
                        "data": self.father.framework.machine.set_data(self.father.framework.machine.info["g5x_index"]),
                        "linear_units": inifile.find("TRAJ", "LINEAR_UNITS") or "mm",
                        "angular_units": inifile.find("TRAJ", "ANGULAR_UNITS") or "degree",
                        "estop": self.father.framework.machine.info["estop"],
                        "paused": self.father.framework.machine.info["paused"],
                        "enabled": self.father.framework.machine.info["enabled"],
                        "state": self.father.framework.machine.info["state"],
                        "interp_state": self.father.framework.machine.info["interp_state"],
                        "task_state": self.father.framework.machine.info["task_state"],
                        "homed": self.father.framework.machine.info["homed"],
                        "is_homed": self.father.framework.armcnc.command.is_homed(),
                        "motion_line": self.father.framework.machine.info["motion_line"],
                        "current_velocity": float(self.father.framework.machine.info["current_vel"]),
                        "spindle": {
                            "enabled": self.father.framework.machine.info["spindle"][0]["enabled"],
                            "direction": self.father.framework.machine.info["spindle"][0]["direction"],
                            "velocity": self.father.framework.machine.info["spindle"][0]["speed"],
                            "min_velocity": int(inifile.find("SPINDLE_0", "MIN_FORWARD_VELOCITY") or 0),
                            "max_velocity": int(inifile.find("SPINDLE_0", "MAX_FORWARD_VELOCITY") or 24000),
                            "min_override": float(inifile.find("DISPLAY", "MIN_SPINDLE_OVERRIDE")),
                            "max_override": float(inifile.find("DISPLAY", "MAX_SPINDLE_OVERRIDE")),
                            "override": self.father.framework.machine.info["spindle"][0]["override"],
                            "override_enabled": self.father.framework.machine.info["spindle"][0]["override_enabled"]
                        },
                        "feed": {
                            "max_override": float(inifile.find("DISPLAY", "MAX_FEED_OVERRIDE")),
                            "override": float(self.father.framework.machine.info["feedrate"])
                        },
                        "max_velocity": float(self.father.framework.machine.info["max_velocity"]),
                        "max_linear_velocity": float(inifile.find("DISPLAY", "MAX_LINEAR_VELOCITY")),
                        "default_linear_velocity": float(inifile.find("DISPLAY", "DEFAULT_LINEAR_VELOCITY")),
                        "max_angular_velocity": float(inifile.find("DISPLAY", "MAX_ANGULAR_VELOCITY")),
                        "default_angular_velocity": float(inifile.find("DISPLAY", "DEFAULT_ANGULAR_VELOCITY"))
                    }

                    self.father.framework.machine.axes = user_data["axes"]

                    axis_tmp = copy.copy(self.father.framework.machine.info["axis"])
                    g_offset_tmp = copy.copy(self.father.framework.machine.info["actual_position"])
                    g5x_offset_tmp = copy.copy(self.father.framework.machine.info["g5x_offset"])
                    g92_offset_tmp = copy.copy(self.father.framework.machine.info["g92_offset"])
                    dtg_offset_tmp = copy.copy(self.father.framework.machine.info["dtg"])
                    for i in range(0, len(user_data["axes"])):
                        actual_position = self.father.framework.machine.info["actual_position"]
                        axis_name = user_data["axes"][i]
                        axis_num = self.father.framework.machine.get_axis_num(axis_name)
                        axis = actual_position[axis_num] - g5x_offset_tmp[axis_num] - self.father.framework.machine.info["tool_offset"][axis_num]
                        axis -= g92_offset_tmp[axis_num]
                        axis = "{:.3f}".format(axis)
                        user_data["data"]["position"][i] = axis
                        g_offset = g_offset_tmp[axis_num]
                        g_offset = "{:.3f}".format(g_offset)
                        user_data["data"]["g_offset"][i] = g_offset
                        g5x_offset = g5x_offset_tmp[axis_num]
                        g5x_offset = "{:.3f}".format(g5x_offset)
                        user_data["data"]["g5x_offset"][i] = g5x_offset
                        g92_offset = g92_offset_tmp[axis_num]
                        g92_offset = "{:.3f}".format(g92_offset)
                        user_data["data"]["g92_offset"][i] = g92_offset
                        dtg_offset = dtg_offset_tmp[axis_num]
                        dtg_offset = "{:.3f}".format(dtg_offset)
                        user_data["data"]["dtg_offset"][i] = dtg_offset
                        user_data["data"]["velocity"][i] = axis_tmp[axis_num]["velocity"]

                    user_data["data"]["tool"] = {
                        "id": self.father.framework.machine.info["tool_table"][0].id,
                        "offset": self.father.framework.machine.info["tool_table"][0].zoffset,
                        "diameter": self.father.framework.machine.info["tool_table"][0].diameter,
                        "item": self.father.framework.machine.info["tool_table"][0]
                    }

                    if user_data["task_state"] == 4:
                        self.father.framework.machine.task_state = True
                    else:
                        self.father.framework.machine.task_state = False

                    self.father.framework.machine.info["user_data"] = user_data

                    self.father.framework.utils.service.service_write({"command": "launch:machine:info", "message": "", "data": self.father.framework.machine.info})
            self.father.framework.utils.set_sleep(0.02)
