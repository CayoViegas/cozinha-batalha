import pygame
import settings

class Boss(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.image = pygame.Surface((128, 128))
        self.image.fill(settings.BLUE)
        self.rect = self.image.get_rect(center=pos)

        # Atributos de combate
        self.name = "Cebola Monstruosa"
        self.health = 300
        self.max_health = 300
        self.attack_power = 20
        self.defense = 10