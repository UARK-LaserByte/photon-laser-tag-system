"""
src/model/player.py

See description below.

by Alex Prosser
11/14/2023
"""


class Player:
    """
    Model that stores all the player information needed for the application
    """

    def __init__(self, player_id: int, equipment_id: int, codename: str, team: str):
        self.player_id: int = player_id
        self.equipment_id: int = equipment_id
        self.codename: str = codename
        self.team: str = team
        self.score: int = 0
        self.reached_base: bool = False

    def __str__(self):
        return f"{self.player_id} : {self.codename} : {self.equipment_id} (Team {self.team})"
