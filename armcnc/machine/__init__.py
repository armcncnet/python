"""
******************************************************************************
* @author  ARMCNC site:www.armcnc.net github:armcnc.github.io
******************************************************************************
"""

import threading
import configparser
import linuxcnc

class Machine:

    def __init__(self, framework):
        self.framework = framework
        self.user = "armcnc"
        self.is_alive = False
        self.stat = None
        self.config = None
        self.config_filter = ["FILTER"]
        self.task = threading.Thread(name="machine_task", target=self.task)
        self.task.daemon = True
        self.task.start()

    def task(self):
        while True:
            if self.is_alive:
                if self.stat and self.stat["ini_filename"] != "":
                    ini_config = configparser.ConfigParser()
                    ini_config.read(self.stat["ini_filename"])
                    if self.config is None:
                        self.config = {}
                    for section in ini_config.sections():
                        if section not in self.config_filter:
                            self.config[section] = {}
                            for key, val in ini_config.items(section):
                                self.config[section][key] = val

                    self.framework.utils.service.service_write({"command": "launch:machine:config", "message": "", "data": self.config})

            self.framework.utils.set_sleep(0.2)
