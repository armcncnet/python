"""
******************************************************************************
* @author  ARMCNC site:www.armcnc.net github:armcnc.github.io
******************************************************************************
"""

import threading
import linuxcnc

class Machine:

    def __init__(self, framework):
        self.framework = framework
        self.user = "armcnc"
        self.is_alive = False
        self.stat = None
        self.config = None
        self.task = threading.Thread(name="machine_task", target=self.task)
        self.task.daemon = True
        self.task.start()

    def task(self):
        while True:
            if self.is_alive:
                self.get_config()
            self.framework.utils.set_sleep(0.5)

    def get_config(self):
        if self.stat and self.stat["ini_filename"] != "":
            config = linuxcnc.ini(self.stat["ini_filename"])
            if self.config is None:
                self.config = {}
            self.config["EMC"] = {
                "MACHINE": config.find("EMC", "MACHINE"),
                "DESCRIBE": config.find("EMC", "DESCRIBE"),
                "CONTROL_TYPE": config.find("EMC", "CONTROL_TYPE"),
                "DEBUG": config.find("EMC", "DEBUG"),
                "VERSION": config.find("EMC", "VERSION"),
            }
            self.config["DISPLAY"] = {
                "DISPLAY": config.find("DISPLAY", "DISPLAY"),
                "CYCLE_TIME": config.find("DISPLAY", "CYCLE_TIME"),
                "POSITION_OFFSET": config.find("DISPLAY", "POSITION_OFFSET"),
                "POSITION_FEEDBACK": config.find("DISPLAY", "POSITION_FEEDBACK"),
                "MAX_FEED_OVERRIDE": config.find("DISPLAY", "MAX_FEED_OVERRIDE"),
                "MAX_SPINDLE_OVERRIDE": config.find("DISPLAY", "MAX_SPINDLE_OVERRIDE"),
                "MAX_LINEAR_VELOCITY": config.find("DISPLAY", "MAX_LINEAR_VELOCITY"),
                "DEFAULT_LINEAR_VELOCITY": config.find("DISPLAY", "DEFAULT_LINEAR_VELOCITY"),
                "DEFAULT_SPINDLE_SPEED": config.find("DISPLAY", "DEFAULT_SPINDLE_SPEED"),
                "PROGRAM_PREFIX": config.find("DISPLAY", "PROGRAM_PREFIX"),
                "INCREMENTS": config.find("DISPLAY", "INCREMENTS"),
            }
            # self.framework.utils.service.service_write({"command": "launch:machine:config", "message": "", "data": self.config})
