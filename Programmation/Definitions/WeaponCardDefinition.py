from Definitions.CardDefinition import CardDefinition, CardPattern, CardRarity


class WeaponCardDefinition(CardDefinition):
    def __init__(self, code: str, name: str, description: str, rarity: CardRarity, cost: int, attack: int, durability: int, image_location: str):
        super().__init__(code, name, description, rarity, cost, CardPattern.WEAPON, image_location)
        self.attack: int = attack
        self.durability: int = durability
