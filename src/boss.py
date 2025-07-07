import pygame
import settings

class Boss(pygame.sprite.Sprite):
    def __init__(self, boss_data, pos, group):
        super().__init__(group)

        size = boss_data["placeholder_size"]
        color = boss_data["placeholder_color"]
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect(center=pos)

        # Atributos de combate
        self.name = boss_data["name"]
        self.health = boss_data["health"]
        self.max_health = boss_data["health"]
        self.attack_power = boss_data["attack_power"]
        self.defense = boss_data["defense"]