import sys
import signal
import launch as launch_file

class Init:

    def __init__(self):
        signal.signal(signal.SIGINT, self.sigint_handler)
        signal.signal(signal.SIGTERM, self.sigint_handler)
        self.setup()

    def setup(self):
        framework_start = "framework_start"
        if framework_start in dir(launch_file):
            getattr(launch_file, framework_start)(self)
        self.sigint_handler(False, False)

    def sigint_handler(self, signum, frame):
        framework_exit = "framework_exit"
        if framework_exit in dir(launch_file):
            getattr(launch_file, framework_exit)(self)
        sys.exit()
