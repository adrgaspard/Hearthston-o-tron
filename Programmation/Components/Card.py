import pygame

from Definitions.MinionCardDefinition import MinionCardDefinition
from Utils.Configuration import Configuration


class Card(pygame.sprite.Sprite):

    def __init__(self, definition: MinionCardDefinition):
        self.definition: MinionCardDefinition = definition
        pygame.sprite.Sprite.__init__(self)
        if Configuration.APP_DRAWING:
            self.image = pygame.image.load(definition.image_location).convert_alpha()
            self.rect = self.image.get_rect()
