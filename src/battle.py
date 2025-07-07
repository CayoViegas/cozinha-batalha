import pygame
import settings
import src.ui as ui

class Battle:
    def __init__(self, player, boss):
        self.player = player
        self.boss = boss

        # Estado da batalha
        self.battle_state = "SELECTING_ACTION"

        # Variáveis de controle do menu
        self.menu_options = ["Atacar", "Defender"]
        self.selected_option = 0

        # Cronometro de turno
        self.turn_timer = None
        self.turn_delay = 1500

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN and self.battle_state == "SELECTING_ACTION":
            # Navegação no menu
            if event.key == pygame.K_RIGHT:
                self.selected_option = (self.selected_option + 1) % len(self.menu_options)
            elif event.key == pygame.K_LEFT:
                self.selected_option = (self.selected_option - 1) % len(self.menu_options)

            # Confirmação da ação
            elif event.key == pygame.K_x:
                selected_action = self.menu_options[self.selected_option]
                print(f"Ação selecionada: {selected_action}")

                if selected_action == "Atacar":
                    # Lógica do ataque
                    self.boss.health -= self.player.attack_power
                    if self.boss.health <= 0:
                        self.boss.health = 0
                        self.battle_state = "VICTORY"
                    else:
                        self.battle_state = "BOSS_ACTION"
                        self.turn_timer = pygame.time.get_ticks()

                elif selected_action == "Defender":
                    # Lógica da defesa
                    self.player.is_defending = True
                    print("Cozinheiro está se defendendo!")
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

                damage = self.boss.attack_power

                if self.player.is_defending:
                    damage //= 2
                    print("Defesa reduziu o dano!")
                    self.player.is_defending = False

                self.player.health -= damage

                if self.player.health <= 0:
                    self.player.health = 0
                    self.battle_state = "DEFEAT"
                    print("Derrota!")
                else:
                    self.battle_state = "SELECTING_ACTION"

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
        
        if self.battle_state == "SELECTING_ACTION":
            option_x_start = settings.SCREEN_WIDTH // 4
            option_y = panel_top + 40
            spacing = 150

            for i, option in enumerate(self.menu_options):
                text_to_draw = option

                if i == self.selected_option:
                    text_to_draw = f"[ {option} ]"

                ui.draw_text(screen, text_to_draw, 28, option_x_start + (i * spacing), option_y, settings.BLACK)

        elif self.battle_state == "BOSS_ACTION":
            ui.draw_text(screen, "Cebola Monstruosa está atacando...", 24, settings.SCREEN_WIDTH // 2, panel_top + 30, settings.BLACK)

        # Mensagem do Resultado Final
        if self.battle_state == "VICTORY":
            ui.draw_text(screen, "VOCÊ VENCEU!", 24, settings.SCREEN_WIDTH // 2, text_y, settings.BLACK)
        elif self.battle_state == "DEFEAT":
            ui.draw_text(screen, "VOCÊ PERDEU!", 24, settings.SCREEN_WIDTH // 2, text_y, settings.BLACK)