import pygame
import settings
import src.ui as ui

class Battle:
    def __init__(self, player, boss):
        self.player = player
        self.boss = boss

        # Estado da batalha
        self.battle_state = "PLAYER_TURN"

        # Cronometro de turno
        self.turn_timer = None
        self.turn_delay = 1500

    def handle_events(self, event):
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

    def update(self):
        if self.battle_state == "VICTORY":
            return "VICTORY"
        if self.battle_state == "DEFEAT":
            return "DEFEAT"
        
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

        return None

    def draw(self, screen):
        # Desenha o painel
        ui.draw_panel(screen)
            
        # UI do Jogador
        player_ui_pos_x = 105
        player_name_pos_y = 12
        player_bar_pos_y = 25
        player_health_bar_rect = pygame.Rect(player_ui_pos_x - 75, player_bar_pos_y, 150, 20)
        ui.draw_text(screen, self.player.name, 22, player_ui_pos_x, player_name_pos_y, settings.WHITE)
        ui.draw_health_bar(screen, self.player.health, self.player.max_health, player_health_bar_rect)

        # UI do Boss
        boss_ui_pos_x = screen.get_width() - 105
        boss_name_pos_y = 12
        boss_bar_pos_y = 25
        boss_health_bar_rect = pygame.Rect(boss_ui_pos_x - 75, boss_bar_pos_y, 150, 20)
        ui.draw_text(screen, self.boss.name, 22, boss_ui_pos_x, boss_name_pos_y, settings.WHITE)
        ui.draw_health_bar(screen, self.boss.health, self.boss.max_health, boss_health_bar_rect)

        # Mensagem de Ação Dinâmica
        panel_top = settings.SCREEN_HEIGHT - (settings.SCREEN_HEIGHT // 3)
        text_y = panel_top + 30
        if self.battle_state == "PLAYER_TURN":
            ui.draw_text(screen, "Pressione ESPAÇO para atacar!", 24, settings.SCREEN_WIDTH // 2, text_y, settings.BLACK)
        elif self.battle_state == "BOSS_ACTION":
            ui.draw_text(screen, "Cebola Monstruosa está atacando...", 24, settings.SCREEN_WIDTH // 2, text_y, settings.BLACK)

        # Mensagem do Resultado Final
        if self.battle_state == "VICTORY":
            ui.draw_text(screen, "VOCÊ VENCEU!", 24, settings.SCREEN_WIDTH // 2, text_y, settings.BLACK)
        elif self.battle_state == "DEFEAT":
            ui.draw_text(screen, "VOCÊ PERDEU!", 24, settings.SCREEN_WIDTH // 2, text_y, settings.BLACK)