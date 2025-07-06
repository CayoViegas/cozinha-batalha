import pygame
import settings

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.image = pygame.Surface((64, 64))
        self.image.fill(settings.GREEN)
        self.rect = self.image.get_rect(center=pos)