"""
******************************************************************************
* @author  ARMCNC site:www.armcnc.net github:armcnc.github.io
******************************************************************************
"""

import threading
import linuxcnc

class Error:

    def __init__(self, father):
        self.father = father
        self.linuxcnc = linuxcnc
        self.api = self.linuxcnc.error_channel()
        self.task = threading.Thread(name="error_task", target=self.task_work)
        self.task.daemon = True
        self.task.start()

    def task_work(self):
        while True:
            if self.father.framework.machine.is_alive:
                error = self.api.poll()
                if error:
                    kind, text = error
                    if kind in (linuxcnc.NML_ERROR, linuxcnc.OPERATOR_ERROR):
                        self.father.framework.utils.service.service_write({"command": "launch:machine:error", "message": text, "data": kind})
            self.father.framework.utils.set_sleep(0.1)
