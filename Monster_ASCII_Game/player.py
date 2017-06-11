from ascii_game.player import Player
from abc import ABC, abstractmethod

class MonsterGamePlayer(Player):
    def __init__(self, name):
        super().__init__(name)

