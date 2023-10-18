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
        self.task = threading.Thread(name="machine_task", target=self.task)
        self.task.daemon = True
        self.task.start()

    def task(self):
        while True:
            if self.is_alive:
                if self.stat:
                    inifile = linuxcnc.ini(self.stat.ini_filename)
                    print(inifile)
            self.framework.utils.set_sleep(0.2)
