from enum import Enum

import numpy as np

from Components.Card import Card
from Components.Deck import Deck
from Components.Hero import Hero
from Data.DataCollector import DataCollector
from Definitions.MinionCardDefinition import MinionCardEffectTypes
from Player.HumanPlayer import HumanPlayer
from Player.IAPlayer import IAPlayer
from Player.Player import Player
from Utils.Configuration import Configuration
from Utils.DeckGenerator import DeckGenerator
from Utils.Utils import Utils


class GameState(Enum):
    PREPARATION = 0,
    MULLIGAN = 1,
    FIGHT = 2,
    END = 3


class TurnState(Enum):
    BEGIN = 0,
    PLAYER_ACTION = 1,
    END = 2


class Game:

    def __init__(self, player_human: bool, deck: Deck):
        self.game_state = GameState.PREPARATION
        self.player_human: bool = player_human
        self.current_player = None
        self.current_turn: int = 0

        # Choix du joueur qui commence.
        self.players: [Player] = []
        self.first_player: int = np.random.randint(2, size=1)[0]
        # self.first_player: int = 0
        self.second_player: int = (self.first_player + 1) % 2
        if self.player_human:
            self.players.append(HumanPlayer(self.first_player == 0, DeckGenerator.clone_deck(deck)))
        else:
            self.players.append(IAPlayer(self.first_player == 0, DeckGenerator.clone_deck(deck)))
        self.players.append(IAPlayer(self.first_player == 1, DeckGenerator.clone_deck(deck)))

        # Préparation des decks.
        self.players[0].hero.deck.shuffle()
        self.players[1].hero.deck.shuffle()

        # Setup des opposants mutuels
        self.players[0].hero.set_opponent(self.players[1].hero)
        self.players[1].hero.set_opponent(self.players[0].hero)

        self.graphic = None

    def mulligan(self):
        for i in range(0, 4):
            self.players[0].hero.draw()
            self.players[1].hero.draw()
        # self.players[1].hero.draw()  Le deuxième joueur pioche une carte de plus. -> Enlevé pour équilibrer

    def begin_fight(self):
        self.game_state = GameState.FIGHT
        self.current_player = self.first_player
        self.players[self.second_player].hero.mana -= 1
        self.players[self.second_player].hero.max_mana -= 1

    def play_turn(self):
        self.current_turn += 1
        if self.current_turn > Configuration.MAX_TURNS:  # La partie prend fin sur une égalité si elle est trop longue.
            return self.end_fight()
        if self.current_player is None:
            self.current_player: int = self.first_player
        else:
            self.current_player: int = (self.current_player + 1) % 2
        self.players[self.current_player].hero.begin_turn()
        # self.players[self.current_player].play_turn()
        if (not self.players[0].hero.is_alive) or (not self.players[1].hero.is_alive):
            return self.end_fight()

    def end_fight(self) -> int:  # Renvoi le numéro du joueur qui a gagné.
        if not self.players[0].hero.is_alive:
            self.game_state = GameState.END
            return 1  # Le joueur 0 a gagné.
        if not self.players[1].hero.is_alive:
            self.game_state = GameState.END
            return 0  # Le joueur 1 a gagné.
        if self.current_turn > Configuration.MAX_TURNS:
            self.game_state = GameState.END
            return -1  # Egalité.
        raise SystemError  # N'est pas censé arriver.

    def attack(self, hero_from_index: int, minion_from_index: int, hero_to_index: int, minion_to_index: int) -> bool:
        try:
            if minion_to_index == -1:
                # meaning that we need to attack the hero
                self.players[hero_from_index].hero.get_minion_board(minion_from_index).attack_opponent()
            elif minion_from_index == -1:
                # meaning that we need to attack the hero with the other hero
                self.players[hero_from_index].hero.attack_opponent()
            else:
                self.players[hero_from_index].hero.get_minion_board(minion_from_index).attack_minion(
                    self.players[hero_to_index].hero.get_minion_board(minion_to_index).id)
                return True
        except AttributeError:
            print('AttributeError attack')
            return False
        except IndexError:
            print('IndexError attack')
            return False

    def play_card(self, hero_index: int, card_index_in_hand: int):
        if self.current_player != hero_index:
            print('Not your turn hero : ' + str(hero_index))
            return
        self.players[hero_index].hero.play_card_by_index(card_index_in_hand)

    def attack_enhanced(self, hero: Hero, minion_id: int, opponent: Hero, target_id: int) -> bool:
        try:
            if target_id == -1:
                # meaning that we need to attack the hero
                hero.get_minion(minion_id).attack_opponent()
            elif minion_id == -1:
                # meaning that we need to attack the hero with the other hero
                hero.attack_opponent()
            else:
                hero.get_minion(minion_id).attack_minion(target_id)
                return True
        except AttributeError as error:
            print("[AttributeError] > " + str(error))
            return False
        except IndexError as error:
            print("[IndexError] > " + str(error))
            return False

    # Ceci est l'algorithme aléatoire de résolution du jeu. Il sert à alimenter la base de données.
    def ia_play_random(self):
        for minion in self.players[1].hero.board:
            minion.attack_opponent()

        for card in self.players[1].hero.hand:
            if self.players[1].hero.can_play_card(card):
                self.players[1].hero.play_card(card)
                return

        for minion in self.players[1].hero.board:
            for minionOpp in self.players[0].hero.board:
                if minion.can_attack_minion(minionOpp.id):
                    minion.attack_minion(minionOpp.id)
                    return
        for minion in self.players[1].hero.board:
            minion.attack_opponent()
        self.play_turn()

    # Ceci est l'algorithme intelligent de résolution du jeu. Ce dernier n'a pas de mémoire sur ces actions précédentes
    # qu'il a pu effectuer pendant le tour. Voici le fonctionnement :
    #   Tant que l'on peut jouer des cartes ou que l'on peut attaquer :
    #       Si on peut battre l'adversaire :
    #           Mettre le plus de dégâts possible à l'adversaire
    #           Recommencer la boucle (ne doit jamais arriver en théorie)
    #       Tant que l'on peut jouer des cartes :
    #           Jouer le plus gros serviteur possible
    #       Tant que l'on peut attaquer :
    #           Attaquer de la meilleur façon possible (en fonction des informations fournies par la base de données)
    def ia_play_smart(self):
        cards_playable: [Card] = self.cards_playable()
        attacks_available: [int, int, float] = self.attacks_available()
        print("> Début du tour de l'IA")
        while len(cards_playable) > 0 or len(attacks_available) > 0:
            print("> L'IA peut jouer des cartes ou attaquer avec un serviteur")
            cards_playable: [Card] = self.cards_playable()
            max_charge_damage_cards: [Card] = self.max_charge_minions_playable()
            print("Nombre de cartes jouables :\n" + str(len(cards_playable)))
            if self.is_lethal():
                print("> L'IA a détecté un lethal")
                self.attack_all_in(max_charge_damage_cards)

            while len(cards_playable) > 0:
                print("> L'IA peut jouer des cartes et va jouer son plus gros serviteur")
                self.play_biggest_minion()
                cards_playable: [Card] = self.cards_playable()
            print("> L'IA ne peut plus jouer de carte et passe en phase d'attaque")
            attacks_available: [int, int, float] = self.attacks_available()
            print("Attaques possibles :\n" + str(attacks_available))
            while len(attacks_available) > 0:
                print("> L'IA va attaquer")
                self.execute_best_movement(attacks_available)
                attacks_available: [int, int, float] = self.attacks_available()
                # Pour l'animation
                self.graphic.playAttackSound()
                return

        self.play_turn()

    # Détermine si on peut vaincre l'adversaire pendant ce tour en tenant compte de 3 paramètres :
    # - Les serviteurs sur le plateau pouvant attaquer le héro.
    # - Les cartes en main jouables possédant charge.
    # - Les serviteurs de l'adversaire ayant provocation.
    def is_lethal(self) -> bool:
        hero: Hero = self.players[self.current_player].hero
        opponent: Hero = hero.opponent
        damage_face = 0
        for i in range(len(opponent.board)):
            if opponent.board[i].effects & MinionCardEffectTypes.TAUNT != 0:
                return False
        for i in range(len(hero.board)):
            if hero.board[i].can_attack_hero():
                damage_face += hero.board[i].attack
        charge_cards = self.max_charge_minions_playable()
        for i in range(len(charge_cards)):
            damage_face += charge_cards[i].definition.attack
        return damage_face >= opponent.health

    # Fait en sorte d'infliger le plus de dégât possible au héro adverse.
    def attack_all_in(self, charge_cards_playable):
        hero: Hero = self.players[self.current_player].hero
        for card in charge_cards_playable:
            hero.play_card(card)
        for minion in hero.board:
            minion.attack_opponent()
            # Pour l'animation
            self.graphic.playAttackSound()
            return

    # Enumère toutes les cartes jouables
    def cards_playable(self) -> [Card]:
        cards_playable = []
        hero: Hero = self.players[self.current_player].hero
        for i in range(len(hero.hand)):
            if hero.hand[i].definition.cost <= hero.mana:
                cards_playable.append(hero.hand[i])
        return cards_playable

    # Retourne le maximum de serviteurs avec charge jouables en tenant compte de la place sur le plateau, du mana
    # disponible, de sorte à ce que les dégats de charge soient les plus importants possibles.
    def max_charge_minions_playable(self) -> [Card]:
        hero: Hero = self.players[self.current_player].hero
        nb_pos_free = Configuration.BOARD_SIZE - len(hero.board)
        cards_to_play: [Card] = []
        charge_cards_playable: [Card] = []
        for i in range(len(hero.hand)):
            if hero.hand[i].definition.effects & MinionCardEffectTypes.CHARGE != 0 and hero.hand[i].definition.cost <= hero.mana:
                charge_cards_playable.append(hero.hand[i])
        if nb_pos_free == 0 or len(charge_cards_playable) == 0:
            return []
        if len(charge_cards_playable) == 1:
            return charge_cards_playable
        if nb_pos_free == 1:
            max_attack = -1
            max_attack_index = -1
            for i in range(len(charge_cards_playable)):
                if charge_cards_playable[i].definition.attack > max_attack:
                    max_attack = charge_cards_playable[i].definition.attack
                    max_attack_index = i
            return [charge_cards_playable[max_attack_index]]
        for i in range(nb_pos_free * len(charge_cards_playable) * 2):
            charges = charge_cards_playable.copy()
            nb_pos_remaining = nb_pos_free
            total_mana = 0
            while nb_pos_remaining > 0 and total_mana < hero.mana:
                cardToAdd = charges[np.random.randint(0, len(charges), 1)]
                if hero.mana - total_mana >= cardToAdd.definition.cost:
                    charges.remove(cardToAdd)
                    cards_to_play[i].append(cardToAdd)
                    nb_pos_remaining -= 1
                else:
                    break
        max_attack = -1
        max_attack_index = -1
        for i in range(len(cards_to_play)):
            total_attack = 0
            for j in range(len(cards_to_play[i])):
                total_attack += cards_to_play[i][j].definition.attack
            if total_attack > max_attack:
                max_attack = total_attack
                max_attack_index = i
        return cards_to_play[max_attack_index]

    # Le premier int retourné : id du minion qui attaque avec le movement.
    # Le deuxième int retourné : id du minion attaqué, ou -1 si c'est le héro adverse.
    # Le float : Winrate de l'attaque.
    def attacks_available(self) -> [[int, int, float]]:
        data_collector: DataCollector = DataCollector()
        attacks: [[int, int, float]] = []
        hero: Hero = self.players[self.current_player].hero
        opponent: Hero = hero.opponent
        for h in range(len(hero.board)):
            for o in range(-1, len(opponent.board)):
                attacker = hero.board[h]
                if o == -1:
                    if attacker.can_attack_hero():
                        attacks.append([attacker.id, -1, data_collector.get_winrate_face_movement(attacker.attack, opponent.health)])
                else:
                    if not attacker.can_attack_any_minion():
                        break
                    opponent_minion = opponent.board[o]
                    if attacker.can_attack_minion(opponent_minion.id):
                        attacker_effects = int(Utils.polish_minion_effect_type(attacker.effects))
                        opponent_minion_effects = int(Utils.polish_minion_effect_type(opponent_minion.effects))
                        attacks.append([attacker.id, opponent_minion.id, data_collector.get_winrate_trade_movement(attacker.attack, attacker.health,
                                                                                                                   attacker_effects,
                                                                                                                   opponent_minion.attack,
                                                                                                                   opponent_minion.health,
                                                                                                                   opponent_minion_effects)])
        return attacks

    # Joue le plus gros serviteur qu'il est possible de joueur
    def play_biggest_minion(self):
        hero: Hero = self.players[self.current_player].hero
        max_cost = -1
        max_cost_index = -1
        for i in range(len(hero.hand)):
            if max_cost < hero.hand[i].definition.cost <= hero.mana:
                max_cost = hero.hand[i].definition.cost
                max_cost_index = i
        if max_cost_index > -1:
            hero.play_card_by_index(max_cost_index)

    # Le premier int de movements : id du minion qui attaque avec le movement.
    # Le deuxième int de movements : id du minion attaqué, ou -1 si c'est le héro adverse.
    # Le float de movements : Winrate de l'attaque.
    def execute_best_movement(self, movements: [int, int, float]):
        hero: Hero = self.players[self.current_player].hero
        opponent: Hero = hero.opponent
        best_movement_index = -1
        best_movement_winrate = -1
        for i in range(len(movements)):
            if movements[i][2] > best_movement_winrate:
                best_movement_index = i
                best_movement_winrate = movements[i][2]
                if best_movement_winrate >= 1:
                    break
        self.attack_enhanced(hero, movements[best_movement_index][0], opponent, movements[best_movement_index][1])
