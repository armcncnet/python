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
        self.api = None
        self.task = threading.Thread(name="status_task", target=self.task)
        self.task.daemon = True
        self.task.start()

    def task(self):
        while True:
            if self.framework.machine.is_alive:
                try:
                    self.api = linuxcnc.stat()
                    status = self.api.poll()
                    # print(status.ini_filename)
                except linuxcnc.error as detail:
                    self.framework.utils.service.service_write({"command": "launch:error", "message": detail, "data": False})

                print(status)

            self.framework.utils.set_sleep(10)
