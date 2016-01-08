"""Contain a class for players"""

class Player(object):
    """A simple Player Object"""

    def __init__(self, name, team, connection):
        self.current_battle = None
        self.name = name
        self.team = team
        self.status = None
        self.position = tuple()
        self.connection = connection
