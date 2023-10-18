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
        self.task = threading.Thread(name="machine_task", target=self.task)
        self.task.daemon = True
        self.task.start()

    def task(self):
        while True:
            if self.is_alive:
                if self.stat and self.stat["ini_filename"] != "":
                    inifile = linuxcnc.ini(self.stat["ini_filename"])
                    if self.config is None:
                        self.config = {}
                    self.config["EMC"] = inifile.findall("EMC")

                    self.framework.utils.service.service_write({"command": "launch:machine:config", "message": "", "data": self.config})

            self.framework.utils.set_sleep(0.2)
