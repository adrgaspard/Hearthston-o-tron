class Configuration:
    # Constantes pour les images

    IMAGE_HUMAN_HERO = "Resources/Images/Heros/HeroHuman.png"
    IMAGE_IA_HERO = "Resources/Images/Heros/HeroIA.png"
    IMAGE_SELECTED_HERO = "Resources/Images/Heros/SelectedHero.png"
    IMAGE_READY_HERO = "Resources/Images/Heros/HeroReady.png"
    IMAGE_BOARD = "Resources/Images/Board.png"
    IMAGE_CARD_BACK = "Resources/Images/Cards/CardBack.png"
    END_TOUR_BUTTON = "Resources/Images/Buttons/end_tour.png"
    END_TOUR_BUTTON_NA = "Resources/Images/Buttons/end_tour_NA.png"
    IMAGE_TAUNT = "Resources/Images/Cards/taunt.png"
    IMAGE_DEVINE_SHIELD = "Resources/Images/Cards/devine_shield.png"
    IMAGE_READY_ATTACK_MINION = "Resources/Images/Cards/readyAttackMinion.png"
    IMAGE_READY_ATTACK_HERO = "Resources/Images/Cards/readyAttackHero.png"
    IMAGE_SELECTED_CARD = "Resources/Images/Cards/selectedCard.png"
    IMAGE_TARGETED_CARD = "Resources/Images/Cards/targetedCard.png"
    IMAGE_LOADING = "Resources/Images/Loadings/Loading"
    IMAGE_WON_IA = "Resources/Images/Won_IA.png"
    IMAGE_WON_PLAYER = "Resources/Images/Won_Player.png"


    # Constantes pour les fichiers.

    CSV_SEPARATOR = ","
    CARD_DEFINITIONS_PATH = "Data/CardDefinitions.csv"
    ACTION_DEFINITIONS_PATH = "Data/ActionDefinitions.csv"
    DATABASE_PATH = "Data/movementData.sqlite"

    # Constantes pour les polices

    MAIN_FONT = "Resources/Fonts/BelweLight.ttf"
    MAIN_FONT_SIZE = 50
    LITTLE_FONT_SIZE = 20
    MAIN_FONT_BLACK = (0, 0, 0)
    MAIN_FONT_WHITE = (255, 255, 255)

    WINNING_FONT = "Resources/Fonts/Sketch.ttf"


    # Constantes pour les sons

    SOUND_MAIN_THEME = "Resources/Sounds/Musics/MainTheme"
    SOUND_WELCOME = "Resources/Sounds/Welcome/Welcome"
    SOUND_ATTACK = "Resources/Sounds/Effects/Attack"

    SOUND_TRAVAIL_TERMINE = "Resources/Sounds/Effects/TravailTermine.wav"
    SOUND_ADD_CARD_TO_HAND = "Resources/Sounds/Effects/AddCardToHand.ogg"
    SOUND_WON = "Resources/Sounds/Effects/Won.ogg"


    SOUND_VOLUME_MUSIC = 0.2
    SOUND_VOLUME_EFFECT = 0.4


    NB_SOUND_TO_LOAD = 2

    # Constantes pour le mulligan.

    MULLIGAN_SIZE_WHEN_FIRST = 3
    MULLIGAN_SIZE_WHEN_SECOND = 4
    COIN_ID = "coin"

    # Constantes pour les joueurs.

    HERO_BASE_HEALTH = 30
    HERO_BASE_ATTACK = 0
    HERO_BASE_MANA = 1
    HERO_MANA_INCREMENT = 1
    HERO_MAX_MANA = 10
    FIRST_HERO_CARD_QUANTITY = 3
    SECOND_HERO_CARD_QUANTITY = 4
    FATIGUE_BASE_DAMAGE = 0

    # Constantes pour la partie.

    MAX_TURNS = 90
    BOARD_SIZE = 7

    # Constantes des decks.

    DECK_SIZE = 30

    # Constantes pour pygame

    APP_DRAWING = True

    TOP = 'TOP'
    BOTTOM = 'BOTTOM'

    FULLSCREEN = False


    # APP_SCALE = 1.3
    APP_SCALE = 1

    WINDOW_TITLE = 'Hearthston-o-tron'
    WINDOW_WIDTH = int(1280 * APP_SCALE)
    WINDOW_HEIGHT = int(720 * APP_SCALE)

    # HERO_SCALE = 0.7
    HERO_SCALE = 1
    HERO_WIDTH = 243
    HERO_HEIGHT = 280
    HERO_SIZE = int(HERO_WIDTH * HERO_SCALE), int(HERO_HEIGHT * HERO_SCALE)

    HERO_HUMAN_POSITION = WINDOW_WIDTH * 0.8 - (HERO_WIDTH * HERO_SCALE / 2), (
            WINDOW_HEIGHT - HERO_HEIGHT * HERO_SCALE) - 30
    HERO_IA_POSITION = WINDOW_WIDTH * 0.8 - (HERO_WIDTH * HERO_SCALE / 2), 30

    HERO_HUMAN_HEALTH_POSITION = HERO_HUMAN_POSITION[0] + HERO_WIDTH * HERO_SCALE - 40, HERO_HUMAN_POSITION[
        1] + HERO_HEIGHT * HERO_SCALE - 50
    HERO_IA_HEALTH_POSITION = HERO_IA_POSITION[0] + HERO_WIDTH * HERO_SCALE - 40, HERO_IA_POSITION[
        1] + HERO_HEIGHT * HERO_SCALE - 50

    # CARD_SCALE = 1
    CARD_SCALE = 1
    CARD_WIDTH = int(150 * CARD_SCALE)
    CARD_HEIGHT = int(204 * CARD_SCALE)

    CARD_SIZE = CARD_WIDTH, CARD_HEIGHT

    CARD_RELATIVE_ATTACK_POSITION = CARD_WIDTH * 0.12, CARD_HEIGHT * 0.82
    CARD_RELATIVE_LIFE_POSITION = CARD_WIDTH * 0.85, CARD_HEIGHT * 0.82


    DECK_TOP_POSITION = WINDOW_WIDTH - CARD_WIDTH - 30, 30
    DECK_BOTTOM_POSITION = WINDOW_WIDTH - CARD_WIDTH - 30, WINDOW_HEIGHT - CARD_HEIGHT - 30

    DECK_TEXT_TOP_POSITION = (DECK_TOP_POSITION[0] + CARD_WIDTH / 2 - 20, DECK_TOP_POSITION[1] + CARD_HEIGHT / 2 - 25)
    DECK_TEXT_BOTTOM_POSITION = (
        DECK_BOTTOM_POSITION[0] + CARD_WIDTH / 2 - 20, DECK_BOTTOM_POSITION[1] + CARD_HEIGHT / 2 - 25)

    CARD_TOP_BOARD_POS = WINDOW_HEIGHT * 1.1 / 3 - CARD_HEIGHT / 2
    CARD_BOTTOM_BOARD_POS = WINDOW_HEIGHT * 1.9 / 3 - CARD_HEIGHT / 2

    CARD_INDEX_BOARD_TOP_POS = [(2 / 11 * WINDOW_WIDTH, CARD_TOP_BOARD_POS),
                                (3 / 11 * WINDOW_WIDTH, CARD_TOP_BOARD_POS),
                                (4 / 11 * WINDOW_WIDTH, CARD_TOP_BOARD_POS),
                                (5 / 11 * WINDOW_WIDTH, CARD_TOP_BOARD_POS),
                                (6 / 11 * WINDOW_WIDTH, CARD_TOP_BOARD_POS),
                                (7 / 11 * WINDOW_WIDTH, CARD_TOP_BOARD_POS),
                                (8 / 11 * WINDOW_WIDTH, CARD_TOP_BOARD_POS)]

    CARD_INDEX_BOARD_BOTTOM_POS = [(2 / 11 * WINDOW_WIDTH, CARD_BOTTOM_BOARD_POS),
                                   (3 / 11 * WINDOW_WIDTH, CARD_BOTTOM_BOARD_POS),
                                   (4 / 11 * WINDOW_WIDTH, CARD_BOTTOM_BOARD_POS),
                                   (5 / 11 * WINDOW_WIDTH, CARD_BOTTOM_BOARD_POS),
                                   (6 / 11 * WINDOW_WIDTH, CARD_BOTTOM_BOARD_POS),
                                   (7 / 11 * WINDOW_WIDTH, CARD_BOTTOM_BOARD_POS),
                                   (8 / 11 * WINDOW_WIDTH, CARD_BOTTOM_BOARD_POS)]

    CARD_BOTTOM_HAND_POS = WINDOW_HEIGHT - CARD_HEIGHT - 30
    CARD_TOP_HAND_POS = 30

    CARD_INDEX_HAND_BOTTOM_POS = [(1 / 11 * WINDOW_WIDTH * 0.7, CARD_BOTTOM_HAND_POS),
                                  (2 / 11 * WINDOW_WIDTH * 0.7, CARD_BOTTOM_HAND_POS),
                                  (3 / 11 * WINDOW_WIDTH * 0.7, CARD_BOTTOM_HAND_POS),
                                  (4 / 11 * WINDOW_WIDTH * 0.7, CARD_BOTTOM_HAND_POS),
                                  (5 / 11 * WINDOW_WIDTH * 0.7, CARD_BOTTOM_HAND_POS),
                                  (6 / 11 * WINDOW_WIDTH * 0.7, CARD_BOTTOM_HAND_POS),
                                  (7 / 11 * WINDOW_WIDTH * 0.7, CARD_BOTTOM_HAND_POS),
                                  (8 / 11 * WINDOW_WIDTH * 0.7, CARD_BOTTOM_HAND_POS),
                                  (9 / 11 * WINDOW_WIDTH * 0.7, CARD_BOTTOM_HAND_POS),
                                  (10 / 11 * WINDOW_WIDTH * 0.7, CARD_BOTTOM_HAND_POS), ]

    CARD_INDEX_HAND_TOP_POS = [(1 / 11 * WINDOW_WIDTH * 0.7, CARD_TOP_HAND_POS),
                               (2 / 11 * WINDOW_WIDTH * 0.7, CARD_TOP_HAND_POS),
                               (3 / 11 * WINDOW_WIDTH * 0.7, CARD_TOP_HAND_POS),
                               (4 / 11 * WINDOW_WIDTH * 0.7, CARD_TOP_HAND_POS),
                               (5 / 11 * WINDOW_WIDTH * 0.7, CARD_TOP_HAND_POS),
                               (6 / 11 * WINDOW_WIDTH * 0.7, CARD_TOP_HAND_POS),
                               (7 / 11 * WINDOW_WIDTH * 0.7, CARD_TOP_HAND_POS),
                               (8 / 11 * WINDOW_WIDTH * 0.7, CARD_TOP_HAND_POS),
                               (9 / 11 * WINDOW_WIDTH * 0.7, CARD_TOP_HAND_POS),
                               (10 / 11 * WINDOW_WIDTH * 0.7, CARD_TOP_HAND_POS), ]

    NUMBER_OF_CARDS_HAND = len(CARD_INDEX_HAND_BOTTOM_POS)

    END_TOUR_BUTTON_WIDTH = 160
    END_TOUR_BUTTON_HEIGHT = 85

    END_TOUR_BUTTON_POSITION = (
        WINDOW_WIDTH - END_TOUR_BUTTON_WIDTH * 1.2, WINDOW_HEIGHT / 2 - END_TOUR_BUTTON_HEIGHT / 2)

    MANA_TOP_POSITION = (WINDOW_WIDTH * 0.92, WINDOW_HEIGHT * 0.3 - 40)
    MANA_BOTTOM_POSITION = (WINDOW_WIDTH * 0.92, WINDOW_HEIGHT * 0.7 - 20)
