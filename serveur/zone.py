"""Contain a simple zone class"""
from time import time

from game import Game
import maths

class Zone(object):
    """
    A Zone class for the game
    contain a generator callable throught run()
    """
    def __init__(self, team_name, position, radius, id_):
        self._team_name = team_name
        self._gen = self._generator()
        self.position = position
        self.radius = radius
        self. id_ = id_
        self.timer = int()

    def run(self):
        """run the internal generator once"""
        return self._gen.__next__()

    def _generator(self):
        foe_in_zone = False
        while True:
            yield
            foe = self.check_foe_in_zone()

            if foe:
                if foe_in_zone:
                    if self.need_change_team():
                        self.team_name = foe.getTeam()
                else:
                    self.timer = time()
                    foe_in_zone = True
            else:
                foe_in_zone = False


    def check_foe_in_zone(self):
        """Check if any foe is in zone and return the firt one found"""
        for player in Game().get_players_not_in_team(self.team_name):
            if maths.distance(self.position, player.position) < self.radius:
                return player

    def need_change_team(self):
        """return True if a player is in zone more than timeout"""
        return time() - self.timer > Game().params.zone_timeout

