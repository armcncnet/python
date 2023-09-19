import sys
import signal
import app as app_file

class Init:

    def __init__(self):
        signal.signal(signal.SIGINT, self.sigint_handler)
        signal.signal(signal.SIGTERM, self.sigint_handler)
        self.setup()

    def setup(self):
        framework_start = "framework_start"
        if framework_start in dir(app_file):
            getattr(app_file, framework_start)(self)
        self.sigint_handler(False, False)

    def sigint_handler(self, signum, frame):
        framework_exit = "framework_exit"
        if framework_exit in dir(app_file):
            getattr(app_file, framework_exit)(self)
        sys.exit()
