"""
******************************************************************************
* @author  ARMCNC site:www.armcnc.net github:armcnc.github.io
******************************************************************************
"""
import time
from .service import Service
from .log import Log

class Utils:

    def __init__(self, framework):
        self.framework = framework
        self.service = Service(self)
        self.log = Log(self)
        self.time = time

    def get_service_status(self):
        return self.service.status

    def set_sleep(self, seconds):
        self.time.sleep(seconds)
