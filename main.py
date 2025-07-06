import pygame
import sys
import settings
from src.player import Player
from src.boss import Boss
import src.ui as ui

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption("Cozinha de Batalha")
        self.clock = pygame.time.Clock()

        self.all_sprites = pygame.sprite.Group()
        self.player = Player((self.screen.get_width() * 0.25, self.screen.get_height() * 0.5), self.all_sprites)
        self.boss = Boss((self.screen.get_width() * 0.75, self.screen.get_height() * 0.5), self.all_sprites)

    def run(self):
        while True:
            # Tratamento de eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Atualização
            self.all_sprites.update()

            # Desenho
            self.screen.fill(settings.BLACK)
            self.all_sprites.draw(self.screen)
            ui.draw_panel(self.screen)
            
            player_ui_pos_x = 105
            player_name_pos_y = 12
            player_bar_pos_y = 25
            player_health_bar_rect = pygame.Rect(player_ui_pos_x - 75, player_bar_pos_y, 150, 20)
            ui.draw_text(self.screen, self.player.name, 22, player_ui_pos_x, player_name_pos_y, settings.WHITE)
            ui.draw_health_bar(self.screen, self.player.health, self.player.max_health, player_health_bar_rect)

            boss_ui_pos_x = self.screen.get_width() - 105
            boss_name_pos_y = 12
            boss_bar_pos_y = 25
            boss_health_bar_rect = pygame.Rect(boss_ui_pos_x - 75, boss_bar_pos_y, 150, 20)
            ui.draw_text(self.screen, self.boss.name, 22, boss_ui_pos_x, boss_name_pos_y, settings.WHITE)
            ui.draw_health_bar(self.screen, self.boss.health, self.boss.max_health, boss_health_bar_rect)

            pygame.display.flip()
            self.clock.tick(settings.FPS)

if __name__ == "__main__":
    game = Game()
    game.run()