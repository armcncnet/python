"""
******************************************************************************
* @author  ARMCNC site:www.armcnc.net github:armcnc.github.io
******************************************************************************
"""

import threading
import linuxcnc

class Error:

    def __init__(self, framework):
        self.framework = framework
        self.linuxcnc = linuxcnc
        self.api = self.linuxcnc.error_channel()
        self.task = threading.Thread(name="error_task", target=self.task)
        self.task.daemon = True
        self.task.start()

    def task(self):
        while True:
            if self.framework.machine.is_alive:
                error = self.api.poll()
                if error:
                    kind, text = error
                    if kind in (linuxcnc.NML_ERROR, linuxcnc.OPERATOR_ERROR):
                        self.framework.utils.service.service_write({"command": "launch:error", "message": text, "data": False})
            self.framework.utils.set_sleep(0.01)



