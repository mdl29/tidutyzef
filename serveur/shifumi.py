"""contain an implementation of shifumi"""
from battle import Battle

class Shifumi(Battle):
    """
    An basic implementation of a battle, here :
        Shifumi
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if len(self.players) is not 2:
            raise ValueError("May have two players in Shifumi")

    def are_choices_over(self):
        return len(self.choices) == 2

    def end_battle(self, loosers, winners):
        for looser in loosers:
            looser.connection.send_win()

        for winners in winners:
            winners.connection.send_win()

    def is_choice_valid(self, choice):
        if choice in ["pierre", "feuille", "ciseaux"]:
            return True

    def play(self):
        truth_table = {"pierre": "ciseau",
                       "feuille": "pierre",
                       "ciseaux": "feuille"}

        (fst, snd, _) = self.choices.items()
        if fst[1] is snd[1]:
            return (True, [], [])

        if truth_table[fst[1]][1] is snd[1]:
            return (False, fst, snd)

        return (False, [snd[0]], [fst[0]])
