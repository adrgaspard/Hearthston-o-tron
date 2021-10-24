from abc import ABC

from Components.Card import Card
from Components.Deck import Deck
from Components.Entity import Entity
from Components.Minion import Minion
from Components.Weapon import Weapon
from Definitions.ActionTranslator import ActionTranslator
from Definitions.CardDefinition import CardPattern
from Definitions.MinionCardDefinition import MinionCardEffectTypes, MinionCardDefinition
from Definitions.SpellCardDefinition import SpellCardDefinition
from Utils.Configuration import Configuration
from Data.CardDictionary import CardDictionary

import pygame


class Hero(Entity, ABC, pygame.sprite.Sprite):

    def __init__(self, is_first: bool, deck: Deck, is_human: bool):
        if Configuration.APP_DRAWING:
            pygame.sprite.Sprite.__init__(self)

        if is_human:
            super().__init__(Configuration.HERO_BASE_HEALTH, Configuration.HERO_BASE_HEALTH,
                             Configuration.HERO_BASE_ATTACK, Configuration.IMAGE_HUMAN_HERO)
            if Configuration.APP_DRAWING:
                self.image = pygame.image.load(Configuration.IMAGE_HUMAN_HERO).convert_alpha()

        else:
            super().__init__(Configuration.HERO_BASE_HEALTH, Configuration.HERO_BASE_HEALTH,
                             Configuration.HERO_BASE_ATTACK, Configuration.IMAGE_IA_HERO)
            if Configuration.APP_DRAWING:
                self.image = pygame.image.load(Configuration.IMAGE_IA_HERO).convert_alpha()

        self.is_first: bool = is_first
        self.mana: int = Configuration.HERO_BASE_MANA
        self.max_mana: int = Configuration.HERO_BASE_MANA
        self.hand: [Card] = []
        self.deck: Deck = deck
        self.weapon = None
        self.board: [Minion] = []
        self.fatigue: int = Configuration.FATIGUE_BASE_DAMAGE
        self.has_attacked: bool = False
        self.opponent = None
        self.is_alive = True
        self.is_human = is_human

        if Configuration.APP_DRAWING:
            self.rect = self.image.get_rect()
            self.selected = False
            self.targeted = False

    def set_opponent(self, opponent):
        self.opponent: Hero = opponent

    def get_minion(self, minion_id: int) -> Minion:
        for minion in self.board:
            if minion.id == minion_id:
                return minion
        return None

    def begin_mulligan(self) -> [Card]:
        mulligan_cards: [Card] = []
        if self.is_first:
            mulligan_size = Configuration.MULLIGAN_SIZE_WHEN_FIRST
        else:
            mulligan_size = Configuration.MULLIGAN_SIZE_WHEN_SECOND
        for i in range(mulligan_size):
            card_mulligan = self.deck.cards[0]
            self.deck.cards.remove(card_mulligan)
            mulligan_cards.append(card_mulligan)
        return mulligan_cards

    def end_mulligan(self, cards_keep: [Card], cards_returned: [Card]):
        nb_cards_returned: int = len(cards_returned)
        for card in cards_keep:
            self.hand.append(card)
        for i in range(nb_cards_returned):  # Pioche un nombre de carte équivalent au nombre de cartes rejetées...
            self.draw()
        for card in cards_returned:  # ... et remet ensuite les cartes rejetées au mulligan dans le deck.
            self.deck.cards.append(card)
        self.deck.shuffle()
        if not self.is_first:  # Ajout de la carte "La pièce si le joueur est deuxième".
            self.hand.append(CardDictionary().get_card(Configuration.COIN_ID))

    def draw(self):
        if len(self.deck.cards) > 0:
            card_draw = self.deck.cards[0]
            self.deck.cards.remove(card_draw)
            if len(self.hand) < 10:
                self.hand.append(card_draw)
        else:
            self.fatigue += 1

    def begin_turn(self):
        self.has_attacked = False
        self.draw()
        if self.max_mana < Configuration.HERO_MAX_MANA:
            self.max_mana += 1
        self.mana = self.max_mana
        for minion in self.board:
            minion.awake()

    def can_play_card(self, card: Card) -> bool:
        if card.definition.cost > self.mana:  # Vérification universelle, indépendante du pattern de la carte.
            return False

        if card.definition.pattern == CardPattern.MINION:  # Si c'est un serviteur.
            if len(self.board) < Configuration.BOARD_SIZE:
                return True
            else:
                return False

        if card.definition.pattern == CardPattern.WEAPON:  # Aucune autre condition que le coût pour une arme.
            return True

        if card.definition.pattern == CardPattern.SPELL:  # Vérification de la validité des cibles /!\ PAS IMPLEMENTE
            return True

    def play_card(self, card: Card):
        if not self.can_play_card(card):
            return
        self.mana -= card.definition.cost
        if self.hand.__contains__(card):
            self.hand.remove(card)
        if card.definition.pattern == CardPattern.MINION:  # Si c'est un serviteur, le placer sur le board.
            cardDictionary: CardDictionary = CardDictionary()
            minionDefinition: MinionCardDefinition = cardDictionary.get_card(card.definition.code)
            self.board.append(Minion(minionDefinition, self))
        if card.definition.pattern == CardPattern.WEAPON:  # Si c'est une arme, remplace l'ancienne.
            self.weapon = Weapon(card.definition, self)
        if card.definition.pattern == CardPattern.SPELL:  # Si c'est un sort, le lance.
            spell_definition: SpellCardDefinition = card.definition
            for action in spell_definition.actions:
                ActionTranslator.apply_action(action, self)

    def play_card_by_index(self, index: int):
        if index < 0 or index > len(self.hand) - 1:
            return
        self.play_card(self.hand[index])

    def take_damage(self, damage: int, is_toxic: bool):
        if self.health > 0:
            if damage >= self.health:
                self.die()
                return
            else:
                self.health -= damage

    def die(self):
        self.is_alive = False

    def can_attack_opponent(self) -> bool:
        if self.has_attacked:
            return False
        for minion in self.opponent.board:
            if minion.effects & MinionCardEffectTypes.TAUNT != 0:
                return False
        if self.weapon is None and self.attack <= 0:
            return False
        return True

    def can_attack_minion(self, minion_id: int) -> bool:
        if self.has_attacked:
            return False
        if self.weapon is None and self.attack <= 0:
            return False
        opponent_has_taunt: bool = False
        minion_exists: bool = False
        for minion in self.opponent.board:
            if minion.effects & MinionCardEffectTypes.TAUNT != 0:
                if minion.id == minion_id:
                    return True
                opponent_has_taunt = True
            if minion.id == minion_id:
                minion_exists = True
        if opponent_has_taunt or not minion_exists:
            return False
        return True

    def attack_opponent(self):
        if not self.can_attack_opponent():
            return
        if self.weapon is None:
            if self.attack > 0:
                self.opponent.take_damage(self.attack)
                self.take_damage(self.opponent.attack)
        else:
            self.opponent.take_damage(self.attack + self.weapon.attack)
            self.take_damage(self.opponent.attack)
            self.weapon.take_damage(1)
        self.has_attacked = True

    def attack_minion(self, minion_id: int):
        if not self.can_attack_minion(minion_id):
            return
        if self.weapon is None:
            if self.attack > 0:
                self.opponent.get_minion(minion_id).take_damage(self.attack)
                self.take_damage(self.opponent.get_minion(minion_id).attack)
        else:
            self.opponent.get_minion(minion_id).take_damage(self.attack + self.weapon.attack)
            self.take_damage(self.opponent.get_minion(minion_id).attack)
            self.weapon.take_damage(1)
        self.has_attacked = True

    def get_minion_board(self, index: int) -> Minion or None:
        if index < 0 or index > len(self.board) - 1:
            return None
        return self.board[index]
