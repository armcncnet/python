"""
******************************************************************************
* @author  ARMCNC site:www.armcnc.net github:armcnc.github.io
******************************************************************************
"""

import sys
import signal
from .utils import Utils
from .cnc import CNC
import launch as launch_file

class Init:

    def __init__(self):
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        self.utils = Utils(self)
        self.armcnc = CNC(self)
        self.start()

    def start(self):
        armcnc_start = "armcnc_start"
        if armcnc_start in dir(launch_file):
            self.armcnc.start()
            getattr(launch_file, armcnc_start)(self)
        self.signal_handler(False, False)

    def message_handle(self, message):
        if self.armcnc and message["command"]:
            armcnc_message = "armcnc_message"
            if armcnc_message in dir(launch_file):
                getattr(launch_file, armcnc_message)(self, message)

    def signal_handler(self, signum, frame):
        armcnc_exit = "armcnc_exit"
        if armcnc_exit in dir(launch_file):
            getattr(launch_file, armcnc_exit)(self)
        sys.exit()
