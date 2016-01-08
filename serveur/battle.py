"""Contain the battle abstract class"""

from time import time

class Battle(object):
    """An abstract battle class between two players"""

    def __init__(self, players: list):
        self.players = players
        self.choices = dict()
        self.reset_timer()
        self._gen = self._generator()
        self.timeout = 500 #in seconds

    def __contains__(self, player):
        if player in self.players:
            return True
        return False

    def set_player_choice(self, player, choice: str):
        """set the choice for player, if valid"""
        if player not in self and self.is_choice_valid(choice):
            player[choice] = choice
            return True

        return False

    def is_choice_valid(self, choice):
        """return True if the choice is a valid choice, otherwise, false"""
        raise NotImplementedError

    def are_choices_over(self):
        """Check if all players played"""
        raise NotImplementedError

    def is_time_over(self):
        """Check time"""
        return time() - self._time < self.timeout

    def reset_timer(self):
        """reset the internal timer"""
        self._time = time()

    def play(self):
        """
        Check winners and loosers
        return : (continue_ : Bool -> True is game is not ended, otherwise, False,
                  winners : [Player],
                  loosers : [Player])
        """
        raise NotImplementedError

    @staticmethod
    def end_battle(loosers, winners):
        """Set status of players and say it to players"""
        for looser in loosers:
            looser.connection.send_win()

        for winners in winners:
            winners.connection.send_win()

    def run(self):
        """A wrapper arround an asynchronic method which do all verifications needed"""
        return self._gen.__next__()

    def _generator(self):
        """An asynchronic method which do all verifications needed"""
        while True: #wait for players
            yield True# bring back hand to the main (game i think)

            if self.is_time_over():
                #TODO: send TimeOver and kill players
                break

            if self.are_choices_over():
                (continue_, winners, loosers) = self.play()
                if continue_:
                    self.reset_timer()
                    continue
                self.end_battle(winners, loosers)
                break
        yield False
