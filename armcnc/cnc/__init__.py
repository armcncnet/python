from .status import Status
from .command import Command
from .ini_file import INIFile
from .error_channel import ErrorChannel

class CNC:

    def __init__(self, framework):
        self.framework = framework
        self.status = Status()
        self.command = Command()
        self.ini_file = INIFile()
        self.error_channel = ErrorChannel()
