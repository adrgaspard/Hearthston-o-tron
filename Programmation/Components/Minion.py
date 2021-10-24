from abc import ABC

import pygame

from Components import Hero
from Components.Entity import Entity
from Definitions.MinionCardDefinition import MinionCardEffectTypes, MinionCardDefinition
from Utils.Configuration import Configuration


class Minion(Entity, ABC, pygame.sprite.Sprite):
    MinionID = 0

    def __init__(self, definition: MinionCardDefinition, master: Hero):
        super().__init__(definition.health, definition.health, definition.attack, definition.image_location)
        self.effects: MinionCardEffectTypes = definition.effects
        self.sleep: bool = self.effects & MinionCardEffectTypes.CHARGE == 0
        self.rush: bool = self.effects & (MinionCardEffectTypes.RUSH + MinionCardEffectTypes.CHARGE) != 0
        self.id: int = Minion.MinionID
        self.master: Hero = master
        Minion.MinionID += 1
        if Configuration.APP_DRAWING:
            self.image = pygame.image.load(definition.image_location).convert_alpha()
            self.rect = self.image.get_rect()
            self.selected: bool = False
            self.targeted: bool = False

    def take_damage(self, damage: int, is_toxic: bool):
        if self.effects & MinionCardEffectTypes.DIVINE_SHIELD != 0:
            self.effects -= MinionCardEffectTypes.DIVINE_SHIELD
        else:
            if self.health > 0:
                if damage >= self.health:
                    self.die()
                    return
                else:
                    self.health -= damage
            if is_toxic:
                self.die()

    def die(self):
        try:
            self.master.board.remove(self)
        except ValueError:
            None
        del self

    def awake(self):
        self.sleep = False

    def can_attack_hero(self) -> bool:
        if self.sleep:
            return False
        for minion in self.master.opponent.board:
            if minion.effects & MinionCardEffectTypes.TAUNT != 0:
                return False
        return True

    def can_attack_any_minion(self) -> bool:
        if len(self.master.opponent.board) == 0:
            return False
        if self.sleep and not self.rush:
            return False
        return True

    def can_attack_minion(self, minion_id: int) -> bool:
        opponent_has_taunt: bool = False
        minion_exists: bool = False
        for minion in self.master.opponent.board:
            if minion.effects & MinionCardEffectTypes.TAUNT != 0:
                if minion.id == minion_id:
                    return True
                opponent_has_taunt = True
            if minion.id == minion_id:
                minion_exists = True
        if opponent_has_taunt or not minion_exists:
            return False
        if self.sleep and not self.rush:
            return False
        return True

    def attack_opponent(self):
        if not self.can_attack_hero():
            return
        if self.attack > 0:
            self.master.opponent.take_damage(self.attack, self.effects)
            # self.take_damage(self.master.opponent.attack, self.effects)
        self.rush = False
        self.sleep = True

    def attack_minion(self, minion_id):
        if not self.can_attack_minion(minion_id):
            return
        if self.attack > 0:
            opponentAttack = self.master.opponent.get_minion(minion_id).attack
            self.master.opponent.get_minion(minion_id).take_damage(self.attack,
                                                                   self.effects & MinionCardEffectTypes.TOXIC != 0)
            self.take_damage(opponentAttack, self.effects & MinionCardEffectTypes.TOXIC != 0)
            self.rush = False
            self.sleep = True
