"""
******************************************************************************
* @author  ARMCNC site:www.armcnc.net github:armcnc.github.io
******************************************************************************
"""

import os
import sys
import signal
from .utils import Utils
from .package import Package
from .cnc import CNC
from .machine import Machine
try:
    import launch as launch_file
    launch_file_imported = True
except ImportError:
    launch_file = None
    launch_file_imported = False

class Init:

    def __init__(self):
        if launch_file_imported:
            signal.signal(signal.SIGINT, self.signal_handler)
            signal.signal(signal.SIGTERM, self.signal_handler)
            self.utils = Utils(self)
            self.machine = Machine(self)
            self.armcnc = CNC(self)
            self.package = Package(self)
            self.start()

    def start(self):
        armcnc_start = "armcnc_start"
        if armcnc_start in dir(launch_file):
            var_name = "MACHINE_PATH"
            if var_name in os.environ:
                env_var = os.environ[var_name]
                if env_var != "":
                    self.machine.machine_path = env_var
                    self.armcnc.start()
            getattr(launch_file, armcnc_start)(self)
        self.signal_handler(False, False)

    def message_handle(self, message):
        if message["command"]:
            if self.machine.is_alive:
                self.armcnc.message_callback(message)
            armcnc_message = "armcnc_message"
            if armcnc_message in dir(launch_file):
                getattr(launch_file, armcnc_message)(self, message)

    def signal_handler(self, signum, frame):
        self.utils.service.service_write({"command": "launch:restart", "message": "", "data": False})
        armcnc_exit = "armcnc_exit"
        if armcnc_exit in dir(launch_file):
            getattr(launch_file, armcnc_exit)(self)
        self.machine.is_alive = False
        sys.exit()
