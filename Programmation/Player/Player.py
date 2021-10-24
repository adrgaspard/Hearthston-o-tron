from Components.Deck import Deck
from Components.Hero import Hero


class Player:

    def __init__(self, is_IA, is_first: bool, deck: Deck):
        if is_IA:
            self.hero: Hero = Hero(is_first, deck, False)
        else:
            self.hero: Hero = Hero(is_first, deck, True)
        self.is_IA = is_IA
