"""
Contain the main Game class
"""
from itertools import product
from threading import Thread

from shifumi import Shifumi
from utils import singleton, check_types
import maths
from team import Team
from player import Player
from params import Params

@singleton
class Game(Thread):
    """
    The main class of the game, this class is a singleton
    """
    _instance = None
    def __init__(self):
        self.teams = {"tidu" : Team("tidu"), "tizef": Team("tizef")}
        self.admin = None
        self.battles = []
        self.zones = []
        self.continue_ = True
        self.params = Params()

        super().__init__(daemon=False)

    def stop(self):
        """Stop the thread"""
        self.continue_ = False

    def start_game(self):
        """Start Game and notify players"""
        if self.params.game_started:
            return
        for player in self.get_players():
            player.status = "playing"
        self.params.game_started = True

        self.broadcast({"object": "startGame"})
        self.start()

    @check_types
    def add_player(self, player: Player):
        """Add a player to the game"""
        p_team = player.team
        team = self.teams.get(p_team, None)
        if team:
            ret = self.teams[p_team].add_player(player)
            if ret:
                self.broadcast({
                    "object": "newUser",
                    "user": player.name,
                    "team": p_team})
            return ret
        else:
            return False

    def get_players(self):
        """return all players"""
        return self._get_players(self.teams)

    @staticmethod
    def _get_players(teams):
        sum_ = []
        for team in teams.values():
            sum_ += team.players
        return sum_

    def get_players_not_in_team(self, team_name):
        """return all player except those in team_name"""
        copy = self.teams.copy()
        copy.pop(team_name)
        return self._get_players(copy)

    def get_player_in_team(self, team_name):
        """return all players of a team"""
        return self.teams.get(team_name, []).players

    @check_types
    def remove_player(self, player: Player):
        """Remove player to the game"""
        self.teams[player.team].del_player(player)

    def create_zone(self, team_name, position, radius, id_, zone):
        """Create a new zone of team teamName"""
        self.zones.append(zone(team_name, position, radius, id_))

    def create_battle(self, players, battle_type):
        """create a new battle between players"""
        for battle in self.battles:
            for player in players:
                if player in battle:
                    return

        self.battles.append(battle_type(players))

    def set_player_choice(self, player, choice):
        """Communicate choice to the battle handler"""
        for battle in self.battles:
            if player in battle:
                battle.set_player_choice(player, choice)

    def run(self):
        """The main thread of game"""
        while self.continue_:
            for battle in self.battles:
                if not battle.run():
                    self.battles.pop(self.battles.index(battle))
            self.check_battles()
            for zone in self.zones:
                zone.run()

    def check_battles(self):
        for (player1, player2) in product(self.get_player_in_team('tidu'),
                                          self.get_player_in_team('tizef')):
            if len(player1.position) != 2 or len(player2.position) != 2:
                continue
            if maths.distance(player1.position, player2.position) <= self.params.battle_radius:
                self.create_battle([player1, player2], Shifumi)

    def broadcast(self, msg):
        """send a message to all players"""
        _ = [p.connection.send(msg) for p in self.get_players()]
        if self.admin:
            self.admin.send(msg)
