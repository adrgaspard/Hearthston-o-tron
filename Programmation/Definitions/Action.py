from enum import IntFlag

from Definitions.CardDefinition import TargetTypes


# NE SERA PAS UTILISE AU RENDU DU PROGRAMME : On a pas assez de temps pour utiliser ce contenu mais on fait en sorte
# qu'il pourra l'être dans le futur.

class ActionTypes(IntFlag):
    DAMAGE = 1,
    HEAL = 2,
    SET_ATTACK = 4,
    SET_CURRENT_HEALTH = 8,
    SET_MAX_HEALTH = 16,
    GIVE_EFFECT = 32,
    SILENCE = 64,
    COPY = 128,
    KILL = 256,
    DRAW = 512,
    SPECIAL = 1024,


class Action:

    def __init__(self, code: str, actionType: ActionTypes, target: TargetTypes, value: int):
        self.code: str = code
        self.actionType: ActionTypes = actionType
        self.target: TargetTypes = target
        self.value: int = value
