from abc import ABC

from Components.Deck import Deck
from Player.Player import Player


class IAPlayer(Player, ABC):

    def __init__(self, is_first: bool, deck: Deck):
        super().__init__(True, is_first, deck)
