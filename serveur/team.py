"""
Contain the team class
"""

from player import Player
from utils import check_types

class Team:
    """A simple team class for tidutizef"""
    def __init__(self, name):
        self.players = []
        self.name = name
        self._lock = False

    def lock(self):
        """lock the adding of Players"""
        self._lock = True

    def unlock(self):
        """unlock the adding of Players"""
        self._lock = False

    def reset(self):
        """reset the team (remove all players and unlock)"""
        self.__init__(self.name)

    @check_types
    def add_player(self, player: Player):
        """add a player to players in """
        self.players.append(player)
        return True

    @check_types
    def del_player(self, player: Player):
        """remove player from team"""
        try:
            self.players.remove(player)
        except ValueError:
            return
