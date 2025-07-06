import pygame
import settings

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.image = pygame.Surface((64, 64))
        self.image.fill(settings.GREEN)
        self.rect = self.image.get_rect(center=pos)

        # Atributos de combate
        self.name = "Cozinheiro"
        self.health = 100
        self.max_health = 100
        self.attack_power = 15
        self.defense = 5