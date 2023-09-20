"""
******************************************************************************
* @author  ARMCNC site:www.armcnc.net github:armcnc.github.io
******************************************************************************
"""

import websocket
import threading

class Service:

    def __init__(self, utils):
        self.utils = utils
        self.socket = None
        self.status = False
        self.task = threading.Thread(name="service_work", target=self.service_work)
        self.task.daemon = True
        self.task.start()

    def service_work(self):
        websocket.enableTrace(False)
        self.socket = websocket.WebSocketApp(
            "ws://127.0.0.1:10010/message/service",
            on_message=self.service_message,
            on_error=self.service_error,
            on_close=self.service_close
        )
        self.socket.on_open = self.service_open
        self.socket.run_forever()

    def service_open(self):
        self.status = True
        self.utils.log.info("service_open")

    def service_write(self, message):
        if self.socket is not None and self.status:
            self.socket.send(self.utils.json.dumps(message))

    def service_message(self, ws, message):
        if self.socket is not None and self.status:
            message_json = self.utils.json.loads(message)
            if message_json["command"]:
                self.utils.framework.message_handle(message_json)

    def service_error(self, ws, error):
        self.socket = None
        self.status = False
        self.utils.log.error("service_error")

    def service_close(self):
        self.socket = None
        self.status = False
        self.utils.log.error("service_close")
