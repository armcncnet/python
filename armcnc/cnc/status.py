"""
******************************************************************************
* @author  ARMCNC site:www.armcnc.net github:armcnc.github.io
******************************************************************************
"""

import threading
import linuxcnc

class Status:

    def __init__(self, framework):
        self.framework = framework
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
                    print(detail)
                    self.framework.utils.service.service_write({"command": "launch:machine:error", "message": detail, "data": False})
                self.framework.machine.stat = {}
                for x in dir(self.api):
                    if not x.startswith("_") and not callable(getattr(self.api, x)):
                        self.framework.machine.stat[x] = getattr(self.api, x)
                self.framework.utils.service.service_write({"command": "launch:machine:status", "message": "", "data": self.framework.machine.stat})
            self.framework.utils.set_sleep(0.05)
