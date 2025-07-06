import pygame
import settings

class Boss(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.image = pygame.Surface((128, 128))
        self.image.fill(settings.BLUE)
        self.rect = self.image.get_rect(center=pos)