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
        self.axis = []
        self.axis_tmp = ""
        self.is_alive = False
        self.info = None
        self.machine_path = ""
        self.workspace = "/opt/armcnc"
        self.task_state = False

    def get_num_axis(self, axis):
        self.axis_tmp = ''.join(self.axis)
        num = self.axis_tmp.find(axis.upper())
        return num

    def get_num(self, axis):
        self.axis_tmp = "XYZABCUVW"
        num = self.axis_tmp.find(axis.upper())
        return num

    def get_user_config_value(self, father, value):
        config = configparser.ConfigParser()
        config.read(self.workspace + "/configs/" + self.machine_path + "/machine.user")
        return config[father][value]

    def get_user_config_items(self, father):
        configs = {}
        config = configparser.ConfigParser()
        config.read(self.workspace + "/configs/" + self.machine_path + "/machine.user")
        items = config.items(father)
        for key, val in items:
            if father == "EXTINFO":
                key = "EXTINFO_" + key.upper()
            configs[key] = float(val.strip())
        return configs
