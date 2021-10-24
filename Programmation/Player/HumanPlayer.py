from abc import ABC

from Components.Deck import Deck
from Player.Player import Player


class HumanPlayer(Player, ABC):

    def __init__(self, is_first: bool, deck: Deck):
        super().__init__(False, is_first, deck)
