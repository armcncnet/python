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

    def test(self):
        self.framework.utils.set_sleep(5)
        self.api = linuxcnc.stat()
        cnc_stat = self.api.poll()
        print("-->", cnc_stat)
        file = getattr(cnc_stat, "file")
        print("-->", file)
