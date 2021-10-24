import numpy as np

from Components.Card import Card


class Deck:

    def __init__(self, cards: [Card]):
        self.cards: [Card] = cards
        self.shuffle()

    def shuffle(self):
        np.random.shuffle(self.cards)

    def getNbCard(self):
        return len(self.cards)
