import pygame
import settings

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.image = pygame.Surface((64, 64))
        self.image.fill(settings.GREEN)
        self.rect = self.image.get_rect(center=pos)

        # Atributos de movimento
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

        # Atributos de combate
        self.name = "Cozinheiro"
        self.health = 100
        self.max_health = 100
        self.attack_power = 15
        self.defense = 5
        self.is_defending = False

    def input(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.pos.y -= self.speed * dt
        if keys[pygame.K_DOWN]:
            self.pos.y += self.speed * dt
        if keys[pygame.K_LEFT]:
            self.pos.x -= self.speed * dt
        if keys[pygame.K_RIGHT]:
            self.pos.x += self.speed * dt

        self.rect.center = self.pos

    def update(self, dt):
        self.input(dt)