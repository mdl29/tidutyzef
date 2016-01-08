"""
An abstract class simplifying interface for Player and Admin
"""
import json
from tornado import websocket

import errcode

class WebSocketHandler(websocket.WebSocketHandler):
    """
    manage client connections
    """
    def __init__(self, *args, **kwargs):
        self.callable_from_json = {}
        self.logged = False
        super().__init__(*args, **kwargs)

    def check_origin(self, origin):
        return True

    def send(self, msg):
        """Send to client"""
        try:
            self.write_message(msg)
        except websocket.WebSocketClosedError:
            self.close()

    def data_received(self, data):
        pass

    def on_message(self, msg):
        """
        unparse the JSON
        """
        try:
            data = json.loads(msg)
        except ValueError:
            self.send(errcode.JSON_ERROR)
            return
        self.on_json_received(data)

    def on_json_received(self, data):
        """Call the appropriated fct, if the fonction is defined in self.callable_from_json"""
        obj = data.pop("object")
        if not self.logged and obj != "login":
            self.send(errcode.USERNAME_NOT_SET)
            return

        if obj in self.callable_from_json:
            try:
                fct = self.callable_from_json[obj]
            except TypeError:
                self.send(errcode.JSON_ERROR)
                return
            fct(**data)
        else:
            self.send(errcode.UNKNOW_OBJECT)

    def on_close(self):
        raise NotImplementedError
