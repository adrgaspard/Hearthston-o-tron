import sys
from datetime import datetime

import numpy

from Data.DataSerializer import DataSerializer
from Game import Game, GameState
from Utils.Configuration import Configuration
from Utils.DeckGenerator import DeckGenerator
from tqdm import tqdm
from tqdm import tqdm_gui


class ConsoleGame:

    def __init__(self, verbose: bool, database_register: bool):
        self.dataSerializer = DataSerializer()
        Configuration.APP_DRAWING = False
        self.game = Game(False, DeckGenerator.create_new_deck())
        self.player1Won = 0
        self.player2Won = 0
        self.verbose = verbose
        self.database_register = database_register
        self.time = datetime.now()

    def reset_game(self):
        self.game = Game(False, DeckGenerator.create_new_deck())

    def start_multiple_games(self, number: int, gui: bool, putty_ui: bool):
        if gui:
            for i in tqdm_gui(range(number)):
                self.reset_game()
                self.start_game()
        else:
            print("")
            old_percentage = 0

            for i in (range(number)):
                self.reset_game()
                self.start_game()
                if putty_ui:
                    ratio = int(i / number * 100)
                    percentage = (int(i / number * 10000)) / 100
                    if percentage > old_percentage:
                        old_percentage = percentage
                        c = "Progress : [" + ("█" * (ratio + 1)) + (" " * (99 - ratio)) + "] (" + str(percentage) + "%)\t\t"
                        print(c, end="\r")
                        sys.stdout.flush()
            print("")

    def start_game(self):
        self.game.mulligan()
        self.game.begin_fight()
        while self.game.game_state == GameState.FIGHT:
            self.play_turn()
        if self.verbose:
            print('--------------------')
            print('Player 1 health : ' + str(self.game.players[0].hero.health))
            print('Player 2 health : ' + str(self.game.players[1].hero.health))
        if self.game.players[0].hero.is_alive:
            self.player1Won += 1
            self.dataSerializer.flushQueues(0)
        if self.game.players[1].hero.is_alive:
            self.player2Won += 1
            self.dataSerializer.flushQueues(1)
        self.game.end_fight()

    def play_turn(self):
        if self.verbose:
            print("\tPlayer 1  : " + str(self.game.players[0].hero.health))
            print("\tPlayer 2  : " + str(self.game.players[1].hero.health))

        for minion in self.game.players[self.game.current_player].hero.board:
            if minion.can_attack_hero():
                if self.database_register:
                    self.dataSerializer.addFaceMoveInQueue(self.game.current_player, minion.attack, self.game.players[
                        (self.game.current_player + 1) % 2].hero.health)
                minion.attack_opponent()
                if (not self.game.players[0].hero.is_alive) or (not self.game.players[1].hero.is_alive):
                    return self.game.end_fight()

        self.shuffle_hand(self.game.current_player)
        for card in self.game.players[self.game.current_player].hero.hand:
            if self.game.players[self.game.current_player].hero.can_play_card(card):
                self.game.players[self.game.current_player].hero.play_card(card)

        self.shuffle_board(self.game.current_player)
        for minion in self.game.players[self.game.current_player].hero.board:
            for minionOpp in self.game.players[(self.game.current_player + 1) % 2].hero.board:
                if minion.can_attack_minion(minionOpp.id):
                    if minion.health == 0:
                        print(minion.health)
                    if self.database_register:
                        self.dataSerializer.addTradeMoveInQueue(self.game.current_player, minion.attack, minion.health,
                                                                minion.effects, minionOpp.attack, minionOpp.health,
                                                                minionOpp.effects)
                    minion.attack_minion(minionOpp.id)

        for minion in self.game.players[self.game.current_player].hero.board:
            if minion.can_attack_hero():
                if self.database_register:
                    self.dataSerializer.addFaceMoveInQueue(self.game.current_player, minion.attack, self.game.players[
                        (self.game.current_player + 1) % 2].hero.health)
                minion.attack_opponent()
                if (not self.game.players[0].hero.is_alive) or (not self.game.players[1].hero.is_alive):
                    return self.game.end_fight()

        self.game.play_turn()

    def shuffle_hand(self, player: int):
        numpy.random.shuffle(self.game.players[player].hero.hand)

    def shuffle_board(self, player: int):
        numpy.random.shuffle(self.game.players[player].hero.board)

    def print_statistics(self):
        print("Victoires du joueur 1 : " + str(self.player1Won))
        print("Victoires du joueur 2 : " + str(self.player2Won))
