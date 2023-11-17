"""
******************************************************************************
* @author  ARMCNC site:www.armcnc.net github:armcnc.github.io
******************************************************************************
"""

from .handwheel import HandWheel

class Package:

    def __init__(self, framework):
        self.framework = framework
        self.handwheel = HandWheel(self)
        self.init_status()

    def init_status(self):
        self.handwheel.joy_speed = self.framework.machine.get_user_config_items("HANDWHEEL")
        if self.handwheel.joy_speed["STATUS"] == "YES":
            self.set_status("handwheel", True)

    def set_status(self, package, status):
        if package == "handwheel":
            if status == "YES":
                self.handwheel.start()
            else:
                self.handwheel.stop()
