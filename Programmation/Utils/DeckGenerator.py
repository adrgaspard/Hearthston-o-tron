from Components.Card import Card
from Components.Deck import Deck
from Data.CardDictionary import CardDictionary
from Utils.Configuration import Configuration
from Definitions.CardDefinition import CardDefinition, CardRarity
import numpy as np


class DeckGenerator:

    @staticmethod
    def clone_deck(deckToCopy: Deck) -> Deck:
        card_dictionary: CardDictionary = CardDictionary()
        cards: [Card] = []
        for cardToCopy in deckToCopy.cards:
            cards.append(Card(card_dictionary.get_card(cardToCopy.definition.code)))
        return Deck(cards)

    @staticmethod
    def create_new_deck() -> Deck:
        card_dictionary: CardDictionary = CardDictionary()
        cards: [Card] = []
        cards_taken = 0
        while cards_taken < Configuration.DECK_SIZE:
            code_card_to_add = np.random.randint(1, 70, 1)[0]
            nb_card_similar = 0
            can_be_added = True
            for card_def in card_dictionary.get_cards():
                if card_def.code == code_card_to_add:
                    nb_card_similar += 1
                    if card_dictionary.get_card(code_card_to_add).rarity == CardRarity.LEGENDARY or nb_card_similar >= 2:
                        can_be_added = False
                        break
            if can_be_added:
                cards.append(Card(card_dictionary.get_card(str(code_card_to_add))))
                cards_taken += 1
        return Deck(cards)

    @staticmethod
    def create_stub_deck() -> Deck:
        card_dictionary: CardDictionary = CardDictionary()
        cards = []
        for i in range(1, 70):
            cards.append(Card(card_dictionary.get_card(str(i))))
        return Deck(cards)
