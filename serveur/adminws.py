"""Contain the socket handler for players"""

from game import Game
from websocket  import WebSocketHandler

from zone import Zone

import errcode

class AdminWs(WebSocketHandler):
    """The socket handler for websocket"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.callable_from_json = {"setParams": self.set_params,
                                   "login": self.login,
                                   "logout": self.logout,
                                   "getParams": self.get_params,
                                   "startGame": self.start_game}

    def open(self, *args, **kwargs):
        super().open(*args, **kwargs)
        self.login()

    @staticmethod
    def start_game():
        """start the game"""
        Game().start_game()

    @staticmethod
    def set_params(**kwargs):
        """set params of the game"""
        params = Game().params
        map_ = kwargs.get('map', None)
        if map_:
            params.map_center = (map_['lat'], map_['lng'])

        zones = kwargs.get('zones', [])
        for zone in zones:
            Game().create_zone(zone['team'], tuple(zone['pos']), zone['radius'], zone['id'], Zone)

        timeout = kwargs.get('time')
        params.game_timeout = timeout

    def get_params(self):
        """send to admin all params"""
        pass

    def login(self):
        """Login player and look if username and team are valids"""
        if Game().admin:
            self.send(errcode.USERNAME_ALREADY_SET)
            self.close()
        else:
            Game().admin = self
            self.logged = True

    def logout(self):
        """logout player and remove it from game"""
        self.close()

    def on_close(self):
        print("Admin is exiting...")
        self.logged = False
        Game().admin = None


    def send(self, msg):
        super().send(msg)
        print('Send to Admin : {}'.format(msg))

    def on_message(self, msg):
        print('Send by Admin : {}'.format(msg))
        super().on_message(msg)
