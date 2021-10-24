from enum import IntFlag

from Definitions.CardDefinition import CardDefinition, CardPattern, CardRarity


class MinionCardEffectTypes(IntFlag):
    TAUNT = 1,
    DIVINE_SHIELD = 2,
    RUSH = 4,
    CHARGE = 8,
    TOXIC = 16


class MinionCardDefinition(CardDefinition):
    def __init__(self, code: str, name: str, description: str, rarity: CardRarity, cost: int, attack: int, health: int,
                 effects: MinionCardEffectTypes, image_location: str):
        super().__init__(code, name, description, rarity, cost, CardPattern.MINION, image_location)
        self.attack: int = attack
        self.health: int = health
        self.effects: MinionCardEffectTypes = effects
