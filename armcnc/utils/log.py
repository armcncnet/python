"""
******************************************************************************
* @author  ARMCNC site:www.armcnc.net github:armcnc.github.io
******************************************************************************
"""

import logging
import colorlog

class Log:

    def __init__(self, utils):
        self.utils = utils
        self.logger = logging.getLogger(None)
        self.logger.handlers = []
        self.logger.setLevel(logging.DEBUG)
        console_fmt = "%(log_color)s%(asctime)s %(levelname)s: %(message)s"
        color_config = {
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "purple",
        }
        console_formatter = colorlog.ColoredFormatter(fmt=console_fmt, log_colors=color_config)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

    def debug(self, log):
        self.logger.debug(log)
        self.utils.service.service_write({"command": "launch:debug", "message": log, "data": False})

    def info(self, log):
        self.logger.info(log)
        self.utils.service.service_write({"command": "launch:info", "message": log, "data": False})

    def warning(self, log):
        self.logger.warning(log)
        self.utils.service.service_write({"command": "launch:warning", "message": log, "data": False})

    def error(self, log):
        self.logger.error(log)
        self.utils.service.service_write({"command": "launch:error", "message": log, "data": False})
