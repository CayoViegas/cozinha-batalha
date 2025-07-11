import pygame
import settings
import src.ui as ui

class Battle:
    def __init__(self, player, enemies):
        self.player = player

        self.enemies = pygame.sprite.Group(enemies)

        # Estado da batalha
        self.battle_state = "SELECTING_ACTION"

        # Variáveis de controle do menu
        self.menu_options = ["Atacar", "Defender"]
        self.selected_option = 0

        self.target_index = 0
        self.acting_enemy_index = 0

        # Cronometro de turno
        self.turn_timer = None
        self.turn_delay = 1500

        self.action_text = ""
        self.action_timer = None
        self.action_delay = 1000

    def get_current_target(self):
        return self.enemies.sprites()[self.target_index]

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN and self.battle_state == "SELECTING_ACTION":
            # Navegação no menu
            if event.key == pygame.K_RIGHT:
                self.selected_option = (self.selected_option + 1) % len(self.menu_options)
            elif event.key == pygame.K_LEFT:
                self.selected_option = (self.selected_option - 1) % len(self.menu_options)
            elif event.key == pygame.K_TAB:
                self.target_index = (self.target_index + 1) % len(self.enemies)
                print(f"Novo alvo: {self.get_current_target().name}")

            # Confirmação da ação
            elif event.key == pygame.K_x:
                selected_action = self.menu_options[self.selected_option]
                self.action_text = f"{self.player.name} usou {selected_action}!"
                self.battle_state = "PERFORMING_PLAYER_ACTION"
                self.action_timer = pygame.time.get_ticks()

    def update(self):
        if self.battle_state == "VICTORY":
            return "VICTORY"
        if self.battle_state == "DEFEAT":
            return "DEFEAT"
        
        current_time = pygame.time.get_ticks()

        if self.battle_state == "PERFORMING_PLAYER_ACTION":
            if current_time - self.action_timer > self.action_delay:
                self.execute_player_action()
                
                if self.battle_state != "VICTORY":
                    self.battle_state = "ENEMIES_ACTION"
                    self.acting_enemy_index = 0
                    self.turn_timer = current_time

        if self.battle_state == "ENEMIES_ACTION":
            if current_time - self.turn_timer > self.turn_delay:
                acting_enemy = self.enemies.sprites()[self.acting_enemy_index]
                self.action_text = f"{acting_enemy.name} está atacando!"
                self.battle_state = "PERFORMING_ENEMY_ACTION"
                self.action_timer = current_time

        if self.battle_state == "PERFORMING_ENEMY_ACTION":
            if current_time - self.action_timer > self.action_delay:
                self.execute_enemy_action()
                
                if self.battle_state == "DEFEAT":
                    return
                
                self.acting_enemy_index += 1
                if self.acting_enemy_index >= len(self.enemies):
                    self.battle_state = "SELECTING_ACTION"
                else:
                    self.battle_state = "ENEMIES_ACTION"
                    self.turn_timer = current_time

        return None
    
    def execute_player_action(self):
        selected_action = self.menu_options[self.selected_option]
        if selected_action == "Atacar":
            target_enemy = self.get_current_target()
            target_enemy.health -= self.player.attack_power
            if target_enemy.health <= 0:
                target_enemy.health = 0
                target_enemy.kill()
                if self.target_index >= len(self.enemies):
                    self.target_index = 0

        elif selected_action == "Defender":
            self.player.is_defending = True

        if not self.enemies:
            self.battle_state = "VICTORY"

    def execute_enemy_action(self):
        acting_enemy = self.enemies.sprites()[self.acting_enemy_index]
        damage = acting_enemy.attack_power
        if self.player.is_defending:
            damage //= 2
            self.player.is_defending = False

        self.player.health -= damage

        if self.player.health <= 0:
            self.player.health = 0
            self.battle_state = "DEFEAT"

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

        #total_enemies = len(self.enemies)
        #spacing = settings.SCREEN_WIDTH / (total_enemies + 1)
        #for i, enemy in enumerate(self.enemies):
            #enemy_ui_pos_x = (i + 1) * spacing
            #enemy_bar_rect = pygame.Rect(enemy_ui_pos_x - 75, 25, 150, 20)

            # Destaca a borda do alvo atual
            #border_color = settings.WHITE
            #if i == self.target_index:
            #    border_color = settings.RED # Cor de destaque para o alvo

            #ui.draw_text(screen, enemy.name, 22, enemy_ui_pos_x, 12)
            #ui.draw_health_bar(screen, enemy.health, enemy.max_health, enemy_bar_rect)
            # Desenha a borda de destaque por cima
            #if i == self.target_index and self.battle_state == "SELECTING_ACTION":
            #    pygame.draw.rect(screen, border_color, enemy_bar_rect, 3)

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

                ui.draw_text(screen, text_to_draw, 24, option_x_start + (i * spacing), option_y, settings.BLACK)

        elif self.battle_state in ["PERFORMING_PLAYER_ACTION", "PERFORMING_ENEMY_ACTION"]:
            ui.draw_text(screen, self.action_text, 24, settings.SCREEN_WIDTH // 2, text_y, settings.BLACK)

        # Mensagem do Resultado Final
        if self.battle_state == "VICTORY":
            ui.draw_text(screen, "VOCÊ VENCEU!", 24, settings.SCREEN_WIDTH // 2, text_y, settings.BLACK)
        elif self.battle_state == "DEFEAT":
            ui.draw_text(screen, "VOCÊ PERDEU!", 24, settings.SCREEN_WIDTH // 2, text_y, settings.BLACK)