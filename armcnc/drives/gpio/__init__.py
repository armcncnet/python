"""
******************************************************************************
* @author  ARMCNC site:www.armcnc.net github:armcnc.github.io
******************************************************************************
"""

import os
import sys
import signal
from base import Base
from ...machine import Machine
import armcncio as armcncio_file

class Init:

    def __init__(self):
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        self.coordinates = ""
        self.machine = Machine(None)
        self.base = Base(self)
        self.start()

    def start(self):
        if len(sys.argv) > 0 and sys.argv[0] != "":
            self.coordinates = sys.argv[0]
            on_start = "on_start"
            if on_start in dir(armcncio_file):
                var_name = "MACHINE_PATH"
                if var_name in os.environ:
                    env_var = os.environ[var_name]
                    if env_var != "":
                        self.machine.machine_path = env_var
                        print(self.machine.machine_path)
                getattr(armcncio_file, on_start)(self)
            self.signal_handler(False, False)

    def signal_handler(self, signum, frame):
        on_exit = "on_exit"
        if on_exit in dir(armcncio_file):
            getattr(armcncio_file, on_exit)(self)
        sys.exit()
