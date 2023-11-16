"""
******************************************************************************
* @author  ARMCNC site:www.armcnc.net github:armcnc.github.io
******************************************************************************
"""

import configparser

class Machine:

    def __init__(self, framework):
        self.framework = framework
        self.user = "armcnc"
        self.axes = []
        self.axes_tmp = ""
        self.axis_tmp = ""
        self.is_alive = False
        self.info = None
        self.data = {"index": 0, "position": {}, "velocity": {}, "g_offset": {}, "g5x_offset": {}, "g92_offset": {}, "dtg_offset": {}, "tool": {}, "options": []}
        self.machine_path = ""
        self.workspace = "/opt/armcnc"
        self.task_state = False

    def set_data(self, index):
        self.data["index"] = index
        if len(self.data["options"]) == 0:
            for key, val in enumerate(range(9)):
                if key > 5:
                    self.data["options"].append({"label": "P" + str(key + 1) + " G59." + str((key - 6) + 1), "p_name": "P" + str(key + 1), "value": key + 1, "name": "G59." + str((key - 6) + 1)})
                else:
                    self.data["options"].append({"label": "P" + str(key + 1) + " G5" + str(key + 4), "p_name": "P" + str(key + 1), "value": key + 1, "name": "G5" + str(key + 4)})
        return self.data

    def get_data(self):
        return self.data

    def get_axes_num(self, axes):
        self.axes_tmp = ''.join(self.axes)
        num = self.axes_tmp.find(axes.upper())
        return num

    def get_axis_num(self, axis):
        self.axis_tmp = "XYZABCUVW"
        num = self.axis_tmp.find(axis.upper())
        return num

    def get_axis_name(self, num):
        self.axis_tmp = "XYZABCUVW"
        name = self.axis_tmp[num]
        return name

    def get_user_config_value(self, father, value):
        config = configparser.ConfigParser()
        config.read(self.workspace + "/configs/" + self.machine_path + "/machine.user")
        return config[father][value].strip()

    def get_user_config_items(self, father):
        configs = {}
        config = configparser.ConfigParser()
        config.read(self.workspace + "/configs/" + self.machine_path + "/machine.user")
        items = config.items(father)
        for key, val in items:
            configs[key] = val.strip()
        return configs
