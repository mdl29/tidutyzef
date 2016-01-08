"""Contain the socket handler for players"""

from utils import check_types

from player import Player
from game import Game
from websocket  import WebSocketHandler

import errcode

class PlayerWs(WebSocketHandler):
    """The socket handler for websocket"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player = None
        self.callable_from_json = {"login": self.login,
                                   "logout": self.logout,
                                   "updatePos": self.update_pos,
                                   "choice": self.choice,
                                   "getAllUsers": self.get_all_users}

    def get_all_users(self):
        """send to player all players connected"""
        players = Game().get_players()
        msg = {'object': "usersConnected",
               'tidu': [p.name for p in players if p.team == 'tidu'],
               'tizef': [p.name for p in players if p.team == 'tizef']}
        self.send(msg)

    def reset(self):
        """Reset the socket (recreate a new Player...)"""
        self.player = None
        self.logged = False

    @check_types
    def login(self, username, team):
        """Login player and look if username and team are valids"""
        if self.player:
            self.send(errcode.USERNAME_ALREADY_SET)
        else:
            self.player = Player(username, team, self)
            if not Game().add_player(self.player):
                self.send(errcode.USERNAME_ALREADY_IN_USE)
                self.reset()

        self.logged = True

    def logout(self):
        """logout player and remove it from game"""
        self.close()

    @check_types
    def update_pos(self, lat: float, lng: float):
        """update the player position"""
        self.player.position = (lat, lng)

    def choice(self, choice: str):
        """set choice for battle"""
        Game().set_player_choice(self.player, choice)

    def on_close(self):
        print("player {} of team {} is exiting...".format(self.player.name, self.player.team))
        if self.player:
            self.logout()
            Game().remove_player(self.player)
            self.reset()

    def send(self, msg):
        super().send(msg)
        if self.player:
            print('Send to {} of team {} : {}'.format(self.player.name, self.player.team, msg))

    def on_message(self, msg):
        if self.player:
            print('Send by {} of team {} : {}'.format(self.player.name, self.player.team, msg))
        super().on_message(msg)
