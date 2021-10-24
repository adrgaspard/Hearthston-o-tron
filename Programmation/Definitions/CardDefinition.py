from enum import Enum
from enum import IntFlag


class TargetTypes(IntFlag):
    NONE = 0,  # La carte ne cible personne.
    PLAYER_HERO = 1,  # La carte cible le héro du joueur qui le lance.
    OPPONENT_HERO = 2,  # La carte cible le héro de l'adversaire du joueur qui le lance.
    ALL_HEROES = 1 + 2,  # La carte cible les deux héros.
    ONE_PLAYER_MINION = 4,  # La carte cible un serviteur du joueur qui le lance.
    ONE_OPPONENT_MINION = 8,  # La carte cible un serviteur de l'adversaire du joueur qui le lance.
    ONE_MINION = 4 + 8,  # La carte cible n'importe quel serviteur.
    ALL_PLAYER_MINIONS = 16,  # La carte cible tous les serviteurs du joueur qui le lance.
    ALL_OPPONENT_MINIONS = 32,  # La carte cible tous les serviteur de l'adversaire du joueur qui le lance.
    ALL_PLAYER = 1 + 16,  # La carte cible le héro et les serviteurs du joueur qui le lance.
    ALL_OPPONENT = 2 + 32,  # La carte cible le héro et les serviteurs de l'adversaire du joueur qui le lance.
    ALL_MINIONS = 16 + 32,  # La carte cible tous les serviteurs.
    ALL = 1 + 2 + 16 + 32  # La carte cible les deux héros et tous les serviteurs.


class CardPattern(Enum):
    MINION = 0,
    WEAPON = 1,
    SPELL = 2,


class CardRarity(Enum):
    COMMON = 0,
    RARE = 1,
    EPIC = 2,
    LEGENDARY = 3


class CardDefinition:

    def __init__(self, code: str, name: str, description: str, rarity: CardRarity, cost: int, pattern: CardPattern, image_location: str):
        self.code: str = code
        self.name: str = name
        self.description: str = description
        self.rarity: CardRarity = rarity
        self.cost: int = cost
        self.pattern: CardPattern = pattern
        self.image_location: str = image_location
