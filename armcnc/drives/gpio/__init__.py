"""
******************************************************************************
* @author  ARMCNC site:www.armcnc.net github:armcnc.github.io
******************************************************************************
"""

import os
import sys
import signal
from .base import Base
from ...machine import Machine

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
            var_name = "MACHINE_PATH"
            if var_name in os.environ:
                env_var = os.environ[var_name]
                if env_var != "":
                    self.machine.machine_path = env_var
                    self.base.setup()
                    while True:
                        self.base.loop()
            self.signal_handler(False, False)

    def signal_handler(self, signum, frame):
        if self.base.hal:
            self.base.hal.exit()
        if self.base.gpio:
            self.base.gpio.cleanup()
        sys.exit()
