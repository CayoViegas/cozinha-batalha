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

        # Estado da batalha
        self.battle_state = "PLAYER_TURN"

        # Cronometro de turno
        self.turn_timer = None
        self.turn_delay = 1500

    def run(self):
        while True:
            # Tratamento de eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.battle_state == "PLAYER_TURN":
                        print("Turno do Jogador: Atacando!")
                        self.boss.health -= self.player.attack_power
                        
                        if self.boss.health <= 0:
                            self.boss.health = 0
                            self.battle_state = "VICTORY"
                            print("Vitoria!")
                        else:
                            self.battle_state = "BOSS_ACTION"
                            self.turn_timer = pygame.time.get_ticks()

            # Atualização
            self.all_sprites.update()

            if self.battle_state == "BOSS_ACTION":
                current_time = pygame.time.get_ticks()
                if current_time - self.turn_timer > self.turn_delay:
                    print("Turno do Boss: Ação executada!")
                    self.player.health -= self.boss.attack_power
                    
                    if self.player.health <= 0:
                        self.player.health = 0
                        self.battle_state = "DEFEAT"
                        print("Derrota!")
                    else:
                        self.battle_state = "PLAYER_TURN"

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

            panel_top = settings.SCREEN_HEIGHT - (settings.SCREEN_HEIGHT // 3)
            text_y = panel_top + 30
            if self.battle_state == "PLAYER_TURN":
                ui.draw_text(self.screen, "Pressione ESPAÇO para atacar!", 24, settings.SCREEN_WIDTH // 2, text_y, settings.BLACK)
            elif self.battle_state == "BOSS_ACTION":
                ui.draw_text(self.screen, "Cebola Monstruosa está atacando...", 24, settings.SCREEN_WIDTH // 2, text_y, settings.BLACK)

            if self.battle_state == "VICTORY":
                ui.draw_text(self.screen, "VOCÊ VENCEU!", 24, settings.SCREEN_WIDTH // 2, text_y, settings.BLACK)
            elif self.battle_state == "DEFEAT":
                ui.draw_text(self.screen, "VOCÊ PERDEU!", 24, settings.SCREEN_WIDTH // 2, text_y, settings.BLACK)

            pygame.display.flip()
            self.clock.tick(settings.FPS)

if __name__ == "__main__":
    game = Game()
    game.run()