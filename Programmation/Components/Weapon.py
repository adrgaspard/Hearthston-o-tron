from abc import ABC

from Components.Entity import Entity
# from Components.Hero import Hero
from Definitions.WeaponCardDefinition import WeaponCardDefinition


class Weapon(Entity, ABC):

    def __init__(self, definition: WeaponCardDefinition, owner):
        super().__init__(definition.durability, definition.durability, definition.attack, definition.image_location)
        self.owner = owner

    def take_damage(self, damage: int, is_toxic: bool):
        self.health = self.health - damage
        if self.health < 0:
            self.die()

    def die(self):
        self.owner.weapon = None
        del self

    def can_attack_hero(self) -> bool:
        raise NotImplementedError

    def can_attack_minion(self, minion_id: int) -> bool:
        raise NotImplementedError

    def attack_opponent(self):
        raise NotImplementedError

    def attack_minion(self, minion_id):
        raise NotImplementedError
