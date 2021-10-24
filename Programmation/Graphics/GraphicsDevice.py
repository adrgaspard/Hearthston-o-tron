import random
import pygame

from Components.Card import Card
from Components.Deck import Deck
from Components.Hero import Hero
from Components.Minion import Minion
from Definitions.MinionCardDefinition import MinionCardEffectTypes
from Game import Game
from Utils.Configuration import Configuration
from Utils.DeckGenerator import DeckGenerator


class GraphicsDevice:
    """
        Main class handling the graphics side of the app
    """

    def __init__(self):
        if Configuration.APP_DRAWING:
            # init pygame
            pygame.mixer.pre_init(44100, -16, 1, 512)
            pygame.init()

            # init window
            self.window = pygame.display.set_mode((Configuration.WINDOW_WIDTH, Configuration.WINDOW_HEIGHT), pygame.RESIZABLE | pygame.HWSURFACE | pygame.DOUBLEBUF)
            pygame.display.set_caption(Configuration.WINDOW_TITLE)

            # loading
            self.loading = pygame.transform.scale(pygame.image.load(Configuration.IMAGE_LOADING + str(random.randint(1, 12)) + ".jpg").convert(), (Configuration.WINDOW_WIDTH, Configuration.WINDOW_HEIGHT))
            self.drawLoading()

            # init sound
            pygame.mixer.Channel(0).set_volume(Configuration.SOUND_VOLUME_EFFECT)
            pygame.mixer.Channel(6).set_volume(Configuration.SOUND_VOLUME_MUSIC)
            pygame.mixer.Channel(7).set_volume(Configuration.SOUND_VOLUME_MUSIC)

            pygame.mixer.Channel(6).play(pygame.mixer.Sound(Configuration.SOUND_WELCOME + str(random.randint(1, 13)) + ".ogg"))
            for i in range(1, Configuration.NB_SOUND_TO_LOAD):
                pygame.mixer.Channel(7).queue(pygame.mixer.Sound(Configuration.SOUND_MAIN_THEME + str(random.randint(1, 9)) + ".ogg"))

            # init assets
            self.board = pygame.image.load(Configuration.IMAGE_BOARD).convert()
            self.card_back = pygame.transform.scale(pygame.image.load(Configuration.IMAGE_CARD_BACK).convert_alpha(), Configuration.CARD_SIZE)
            self.card_taunt = pygame.transform.scale(pygame.image.load(Configuration.IMAGE_TAUNT).convert_alpha(), Configuration.CARD_SIZE)
            self.card_devine_shield = pygame.transform.scale(pygame.image.load(Configuration.IMAGE_DEVINE_SHIELD).convert_alpha(), Configuration.CARD_SIZE)
            self.card_ready_attack_hero = pygame.transform.scale(pygame.image.load(Configuration.IMAGE_READY_ATTACK_HERO).convert_alpha(), Configuration.CARD_SIZE)
            self.card_ready_attack_minion = pygame.transform.scale(pygame.image.load(Configuration.IMAGE_READY_ATTACK_MINION).convert_alpha(), Configuration.CARD_SIZE)
            self.end_tour_button = pygame.transform.scale(pygame.image.load(Configuration.END_TOUR_BUTTON).convert_alpha(), (Configuration.END_TOUR_BUTTON_WIDTH, Configuration.END_TOUR_BUTTON_HEIGHT))
            self.end_tour_button_na = pygame.transform.scale(pygame.image.load(Configuration.END_TOUR_BUTTON_NA).convert_alpha(), (Configuration.END_TOUR_BUTTON_WIDTH, Configuration.END_TOUR_BUTTON_HEIGHT))
            self.end_tour_button_rect = pygame.Rect(Configuration.END_TOUR_BUTTON_POSITION, (Configuration.END_TOUR_BUTTON_WIDTH, Configuration.END_TOUR_BUTTON_HEIGHT))
            self.main_font = pygame.font.Font(Configuration.MAIN_FONT, Configuration.MAIN_FONT_SIZE)
            self.little_font = pygame.font.Font(Configuration.MAIN_FONT, Configuration.LITTLE_FONT_SIZE)
            self.winning_font = pygame.font.Font(Configuration.WINNING_FONT, 120)
            self.won_ia = pygame.transform.scale(pygame.image.load(Configuration.IMAGE_WON_IA).convert_alpha(), (Configuration.WINDOW_WIDTH, Configuration.WINDOW_HEIGHT))
            self.won_player = pygame.transform.scale(pygame.image.load(Configuration.IMAGE_WON_PLAYER).convert_alpha(), (Configuration.WINDOW_WIDTH, Configuration.WINDOW_HEIGHT))

            self.card_selected = pygame.transform.scale(pygame.image.load(Configuration.IMAGE_SELECTED_CARD).convert_alpha(), Configuration.CARD_SIZE)
            self.card_targeted = pygame.transform.scale(pygame.image.load(Configuration.IMAGE_TARGETED_CARD).convert_alpha(), Configuration.CARD_SIZE)
            self.hero_selected = pygame.transform.scale(pygame.image.load(Configuration.IMAGE_SELECTED_HERO).convert_alpha(), Configuration.HERO_SIZE)
            self.hero_ready = pygame.transform.scale(pygame.image.load(Configuration.IMAGE_READY_HERO).convert_alpha(), Configuration.HERO_SIZE)

            # init UI tweak
            self.clicked = False
            self.attackChoice = False
            self.attackFromIndex = 0
            self.attackFromHero = Configuration.BOTTOM

            # init game
            self.game = Game(True, DeckGenerator.create_new_deck())
            self.game.graphic = self
            self.player_bottom = self.game.players[0]
            self.player_top = self.game.players[1]

            self.hero_bottom = self.player_bottom.hero
            self.hero_top = self.player_top.hero

    def toggleFullscreen(self):
        """
            Change fullscreen state
        """
        Configuration.FULLSCREEN = not Configuration.FULLSCREEN
        if Configuration.FULLSCREEN:
            infoObject = pygame.display.Info()
            self.window = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), pygame.NOFRAME | pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
        else:
            self.window = pygame.display.set_mode((Configuration.WINDOW_WIDTH, Configuration.WINDOW_HEIGHT), pygame.RESIZABLE | pygame.HWSURFACE | pygame.DOUBLEBUF)

    @staticmethod
    def isMouseInside(event, rect: pygame.rect) -> bool:
        """
            main method to check if mouse is clicking on an image
        :param event: pygame event
        :param rect: rect to check
        :return: true || false
        """
        return rect.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN

    def resetSelected(self):
        """
            reset selected minion in game
        """
        for minion in self.hero_top.board:
            if minion.selected:
                minion.selected = False
        for minion in self.hero_bottom.board:
            if minion.selected:
                minion.selected = False
        self.hero_bottom.selected = False
        self.hero_top.selected = False
        self.attackChoice = False

    def exit(self):
        """
        exit the app
        """
        self.game.end_fight()
        pygame.quit()

    def draw(self):
        """
        draw everything on screen
        """
        self.drawBoard()
        self.drawHero(self.hero_top, True)
        self.drawHero(self.hero_bottom, False)
        self.drawDeck(self.hero_top.deck, Configuration.TOP)
        self.drawDeck(self.hero_bottom.deck, Configuration.BOTTOM)
        self.drawHeroBoard(self.hero_top, Configuration.TOP)
        self.drawHeroBoard(self.hero_bottom, Configuration.BOTTOM)
        self.drawHeroHand(self.hero_top, Configuration.TOP)
        self.drawHeroHand(self.hero_bottom, Configuration.BOTTOM)
        self.drawMana(self.hero_top, Configuration.TOP)
        self.drawMana(self.hero_bottom, Configuration.BOTTOM)
        self.drawEndTourButton()

    def drawHero(self, hero: Hero, top: bool):
        """
            draw a hero to screen
        :param hero: hero to draw
        :param top: is top of not
        """
        image = pygame.transform.scale(hero.image, (int(Configuration.HERO_WIDTH * Configuration.HERO_SCALE), int(Configuration.HERO_HEIGHT * Configuration.HERO_SCALE)))
        health = self.main_font.render(str(hero.health), True, Configuration.MAIN_FONT_WHITE)

        if top:
            if self.game.current_player == 1:
                self.window.blit(self.hero_ready, Configuration.HERO_IA_POSITION)
            self.window.blit(image, Configuration.HERO_IA_POSITION)
            self.window.blit(health, Configuration.HERO_IA_HEALTH_POSITION)
            if hero.selected:
                self.window.blit(self.hero_selected, Configuration.HERO_IA_POSITION)
        else:
            if self.game.current_player == 0:
                self.window.blit(self.hero_ready, Configuration.HERO_HUMAN_POSITION)
            self.window.blit(image, Configuration.HERO_HUMAN_POSITION)
            self.window.blit(health, Configuration.HERO_HUMAN_HEALTH_POSITION)
            if hero.selected:
                self.window.blit(self.hero_selected, Configuration.HERO_HUMAN_POSITION)

    def drawCard(self, card: Card, position: tuple, visible: bool, top: bool):
        """
            draw a card to screen
        :param card: card to draw
        :param position: position (tuple) to draw
        :param visible: visible or not
        :param top: is top or not
        :return: return to avoir NoneType exception
        """
        if visible:
            if card is None:
                return
                # par sécurité pour éviter le nullPointerException

            if top:
                if card.definition.cost <= self.hero_top.mana:
                    self.window.blit(self.card_ready_attack_minion, position)
            else:
                if card.definition.cost <= self.hero_bottom.mana:
                    self.window.blit(self.card_ready_attack_minion, position)

            image = pygame.transform.scale(card.image, Configuration.CARD_SIZE)

            self.window.blit(image, position)
            health = self.little_font.render(str(card.definition.health), True, Configuration.MAIN_FONT_WHITE)
            attack = self.little_font.render(str(card.definition.attack), True, Configuration.MAIN_FONT_WHITE)
            self.window.blit(health, (position[0] + Configuration.CARD_RELATIVE_LIFE_POSITION[0], position[1] + Configuration.CARD_RELATIVE_LIFE_POSITION[1]))
            self.window.blit(attack, (position[0] + Configuration.CARD_RELATIVE_ATTACK_POSITION[0], position[1] + Configuration.CARD_RELATIVE_ATTACK_POSITION[1]))
        else:
            image = pygame.transform.scale(self.card_back, Configuration.CARD_SIZE)
            self.window.blit(image, position)


    def drawMinion(self, minion: Minion, position: tuple):
        """
            draw a minion to screen
        :param minion: minion to draw
        :param position: position (tuple) to draw
        """
        image = pygame.transform.scale(minion.image, Configuration.CARD_SIZE)
        health = self.little_font.render(str(minion.health), True, Configuration.MAIN_FONT_WHITE)
        attack = self.little_font.render(str(minion.attack), True, Configuration.MAIN_FONT_WHITE)

        if minion.can_attack_hero():
            self.window.blit(self.card_ready_attack_hero, position)
        elif minion.can_attack_any_minion():
            self.window.blit(self.card_ready_attack_minion, position)

        self.window.blit(image, position)
        self.window.blit(health, (position[0] + Configuration.CARD_RELATIVE_LIFE_POSITION[0], position[1] + Configuration.CARD_RELATIVE_LIFE_POSITION[1]))
        self.window.blit(attack, (position[0] + Configuration.CARD_RELATIVE_ATTACK_POSITION[0], position[1] + Configuration.CARD_RELATIVE_ATTACK_POSITION[1]))
        if minion.effects & MinionCardEffectTypes.TAUNT != 0:
            self.window.blit(self.card_taunt, position)
        if minion.effects & MinionCardEffectTypes.DIVINE_SHIELD != 0:
            self.window.blit(self.card_devine_shield, position)
        if minion.selected:
            self.window.blit(self.card_selected, position)
        if minion.targeted:
            self.window.blit(self.card_targeted, position)

    def drawBoard(self):
        """
            draw background of the app
        """
        image = pygame.transform.scale(self.board, (Configuration.WINDOW_WIDTH, Configuration.WINDOW_HEIGHT))
        self.window.blit(image, (0, 0))

    def drawDeck(self, deck: Deck, position):
        """
            draw deck to screen
        :param deck: deck to draw
        :param position: postion (string) to draw (Configuration.TOP || Configuration.BOTTOM)
        """
        numberOfCard = self.main_font.render(str(deck.getNbCard()), True, Configuration.MAIN_FONT_BLACK)
        if position == Configuration.TOP:
            self.drawCard(None, Configuration.DECK_TOP_POSITION, False, True)
            self.window.blit(numberOfCard, Configuration.DECK_TEXT_TOP_POSITION)
        else:
            self.drawCard(None, Configuration.DECK_BOTTOM_POSITION, False, False)
            self.window.blit(numberOfCard, Configuration.DECK_TEXT_BOTTOM_POSITION)

    def drawHeroBoard(self, hero: Hero, position):
        """
            draw board of a hero to screen
        :param hero: hero board to draw
        :param position: postion (string) to draw (Configuration.TOP || Configuration.BOTTOM)
        """
        i = 0
        for minion in hero.board:
            if position == Configuration.TOP:
                self.drawMinion(minion, Configuration.CARD_INDEX_BOARD_TOP_POS[i])
            else:
                self.drawMinion(minion, Configuration.CARD_INDEX_BOARD_BOTTOM_POS[i])
            i += 1

    def drawHeroHand(self, hero: Hero, position):
        """
            draw hand of a hero to screen
        :param hero: hero hand to draw
        :param position: postion (string) to draw (Configuration.TOP || Configuration.BOTTOM)
        """
        i = 0
        for card in hero.hand:
            if position == Configuration.TOP:
                self.drawCard(card, Configuration.CARD_INDEX_HAND_TOP_POS[i], False, True)
            else:
                self.drawCard(card, Configuration.CARD_INDEX_HAND_BOTTOM_POS[i], True, False)
            i += 1

    def drawEndTourButton(self):
        """
            draw end tour buton
        """
        if self.game.current_player == 0:
            self.window.blit(self.end_tour_button, Configuration.END_TOUR_BUTTON_POSITION)
        else:
            self.window.blit(self.end_tour_button_na, Configuration.END_TOUR_BUTTON_POSITION)

    def drawMana(self, hero: Hero, position):
        """
            draw mana of a hero to screen
        :param hero: hero mana to draw
        :param position: postion (string) to draw (Configuration.TOP || Configuration.BOTTOM)

        """
        mana = self.main_font.render(str(hero.mana) + "/" + str(hero.max_mana), True, Configuration.MAIN_FONT_WHITE)
        if position == Configuration.TOP:
            self.window.blit(mana, Configuration.MANA_TOP_POSITION)
        else:
            self.window.blit(mana, Configuration.MANA_BOTTOM_POSITION)

    def drawLoading(self):
        """
        draw loading screen
        """
        self.window.blit(self.loading, (0, 0))
        pygame.display.flip()

    def handleDeckClick(self, event):
        """
            method to check if deck is clicked
        :param event: pygame event
        """
        if GraphicsDevice.isMouseInside(event, pygame.Rect(Configuration.DECK_TOP_POSITION, Configuration.CARD_SIZE)):
            self.hero_top.draw()
            pygame.mixer.Channel(0).play(pygame.mixer.Sound(Configuration.SOUND_ADD_CARD_TO_HAND))
            # faire piocher le hér<o du haut
        if GraphicsDevice.isMouseInside(event, pygame.Rect(Configuration.DECK_BOTTOM_POSITION, Configuration.CARD_SIZE)):
            self.hero_bottom.draw()
            pygame.mixer.Channel(0).play(pygame.mixer.Sound(Configuration.SOUND_ADD_CARD_TO_HAND))
            # faire piocher le héro du bas

    def handleHandClick(self, event):
        """
        method to check if minion on hand is clicked
        :param event: pygame event
        """
        for i in range(0, Configuration.NUMBER_OF_CARDS_HAND):
            if GraphicsDevice.isMouseInside(event, pygame.Rect(Configuration.CARD_INDEX_HAND_TOP_POS[i], Configuration.CARD_SIZE)):
                self.game.play_card(1, i)
            if GraphicsDevice.isMouseInside(event, pygame.Rect(Configuration.CARD_INDEX_HAND_BOTTOM_POS[i], Configuration.CARD_SIZE)):
                self.game.play_card(0, i)

    def handleAttack(self, event):
        """
        method to do all the attack system
        :param event: pygame event
        """
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                self.resetSelected()
        if self.attackChoice:
            for i in range(0, Configuration.BOARD_SIZE):
                if GraphicsDevice.isMouseInside(event, pygame.Rect(Configuration.CARD_INDEX_BOARD_TOP_POS[i], Configuration.CARD_SIZE)):
                    if self.attackFromHero == Configuration.BOTTOM:
                        if self.game.attack(0, self.attackFromIndex, 1, i):
                            self.playAttackSound()
                            self.attackChoice = False
                    else:
                        if self.game.attack(1, self.attackFromIndex, 1, i):
                            self.playAttackSound()
                            self.attackChoice = False
                if GraphicsDevice.isMouseInside(event, pygame.Rect(Configuration.CARD_INDEX_BOARD_BOTTOM_POS[i], Configuration.CARD_SIZE)):
                    if self.attackFromHero == Configuration.BOTTOM:
                        if self.game.attack(0, self.attackFromIndex, 0, i):
                            self.playAttackSound()
                            self.attackChoice = False
                    else:
                        if self.game.attack(1, self.attackFromIndex, 0, i):
                            self.playAttackSound()
                            self.attackChoice = False
            if GraphicsDevice.isMouseInside(event, pygame.Rect(Configuration.HERO_IA_POSITION, Configuration.HERO_SIZE)):
                if self.attackFromHero == Configuration.BOTTOM:
                    if self.game.attack(0, self.attackFromIndex, 1, -1):
                        self.playAttackSound()
                        self.attackChoice = False
                if self.attackFromHero == Configuration.TOP:
                    if self.game.attack(1, self.attackFromIndex, 1, -1):
                        self.playAttackSound()
                        self.attackChoice = False
            if GraphicsDevice.isMouseInside(event, pygame.Rect(Configuration.HERO_HUMAN_POSITION, Configuration.HERO_SIZE)):
                if self.attackFromHero == Configuration.BOTTOM:
                    if self.game.attack(0, self.attackFromIndex, 0, -1):
                        self.playAttackSound()
                        self.attackChoice = False
                if self.attackFromHero == Configuration.TOP:
                    if self.game.attack(1, self.attackFromIndex, 0, -1):
                        self.playAttackSound()
                        self.attackChoice = False

        self.handleSelectedMinion()
        self.handleSelectedHero()

        self.handleSelectMinion(event)
        self.handleSelectHero(event)

    def handleSelectMinion(self, event):
        """
        method to handle the selection of minions
        :param event: pygame event
        """
        try:

            if not self.attackChoice:
                for i in range(0, Configuration.BOARD_SIZE):
                    if GraphicsDevice.isMouseInside(event, pygame.Rect(Configuration.CARD_INDEX_BOARD_TOP_POS[i], Configuration.CARD_SIZE)):
                        self.attackFromHero = Configuration.TOP
                        self.attackFromIndex = i
                        self.hero_top.get_minion_board(i).selected = True
                        self.attackChoice = True
                    if GraphicsDevice.isMouseInside(event, pygame.Rect(Configuration.CARD_INDEX_BOARD_BOTTOM_POS[i], Configuration.CARD_SIZE)):
                        self.attackFromHero = Configuration.BOTTOM
                        self.attackFromIndex = i
                        self.hero_bottom.get_minion_board(i).selected = True
                        self.attackChoice = True

        except AttributeError:
            print('Not a valid minion')

    def handleSelectHero(self, event):
        """
        method to handle the selection of heros
        :param event: pygame event
        """
        if not self.attackChoice:
            if GraphicsDevice.isMouseInside(event, pygame.Rect(Configuration.HERO_HUMAN_POSITION, Configuration.HERO_SIZE)):
                self.hero_bottom.selected = True
                self.attackFromHero = Configuration.BOTTOM
                self.attackFromIndex = -1
                self.attackChoice = True
            if GraphicsDevice.isMouseInside(event, pygame.Rect(Configuration.HERO_IA_POSITION, Configuration.HERO_SIZE)):
                self.hero_top.selected = True
                self.attackFromHero = Configuration.BOTTOM
                self.attackFromIndex = -1
                self.attackChoice = True

    def handleSelectedMinion(self):
        """
        method to handle the selected minions
        """
        if not self.attackChoice:
            for minion in self.hero_top.board:
                if minion.selected:
                    minion.selected = False
            for minion in self.hero_bottom.board:
                if minion.selected:
                    minion.selected = False

    def handleSelectedHero(self):
        """
        method to handle the selected heros
        """
        if not self.attackChoice:
            self.hero_bottom.selected = False
            self.hero_top.selected = False

    def handleEndTourButton(self, event):
        """
        handle end tour button
        :param event: pygame event
        """
        if GraphicsDevice.isMouseInside(event, self.end_tour_button_rect):
            if self.game.current_player == 0:
                self.playTravailTermine()
                self.game.play_turn()
                self.resetSelected()

    def handleMouse(self, event):
        """
        handle mouse event
        :param event: pygame event
        """
        self.handleEndTourButton(event)
        self.handleHandClick(event)
        self.handleAttack(event)

    def handleWinning(self):
        """
        handle winnig of a player (text + sound)
        :return:
        """
        if self.hero_top.is_alive and self.hero_bottom.is_alive:
            return
        message = None

        if not self.hero_top.is_alive:
            self.window.blit(self.won_player, (0, 0))
        else:
            self.window.blit(self.won_ia, (0, 0))

        pygame.mixer.Channel(0).play(pygame.mixer.Sound(Configuration.SOUND_WON))

    def handleIAPlays(self, is_smart: bool):
        if self.game.current_player == 1:
            if is_smart:
                self.game.ia_play_smart()
            else:
                self.game.ia_play_random()
            self.sleep()

    def sleep(self):
        pygame.time.wait(1500)

    def playTravailTermine(self):
        """
        play sound "travail terminé"
        """
        pygame.mixer.Channel(0).play(pygame.mixer.Sound(Configuration.SOUND_TRAVAIL_TERMINE))

    def playAttackSound(self):
        """
        play a sound attack randomly
        """
        pygame.mixer.Channel(0).play(pygame.mixer.Sound(Configuration.SOUND_ATTACK + str(random.randint(1, 6)) + ".ogg"))

    def start(self, is_smart: bool):
        """
        start the app
        :return: when app is not in debug mode
        """
        if not Configuration.APP_DRAWING:
            return

        looping = True

        self.game.begin_fight()
        self.game.mulligan()

        while looping:
            self.draw()
            self.handleWinning()
            self.handleIAPlays(is_smart)
            for event in pygame.event.get():
                self.handleMouse(event)
                if event.type == pygame.QUIT:
                    looping = False
                if event.type == pygame.VIDEORESIZE:
                    self.window.fill((255, 255, 255))
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        looping = False
                    if event.key == pygame.K_f:
                        self.toggleFullscreen()

            pygame.display.flip()
