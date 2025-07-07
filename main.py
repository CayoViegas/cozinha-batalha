import pygame
import sys
import settings
import json
from src.player import Player
from src.boss import Boss
from src.battle import Battle

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption("Cozinha de Batalha")
        self.clock = pygame.time.Clock()

        self.game_state = "KITCHEN"
        #self.game_state = "BATTLE"

        self.load_data()

        self.all_sprites = pygame.sprite.Group()
        self.player = Player((self.screen.get_width() * 0.25, self.screen.get_height() * 0.5), self.all_sprites)
        #self.boss = Boss((self.screen.get_width() * 0.75, self.screen.get_height() * 0.5), self.all_sprites)

        self.battle = None
        #self.battle = Battle(self.player, self.boss)

    def load_data(self):
        try:
            with open("data/boss_data.json", "r", encoding="utf-8") as f:
                self.boss_data = json.load(f)
                print("Dados dos bosses carregados com sucesso!")
        except FileNotFoundError:
            print("ERRO: Arquivo 'data/boss_data.json' não encontrado!")
            self.boss_data = {}

    def run(self):
        while True:
            dt = self.clock.tick(settings.FPS) / 1000.0

            # Tratamento de eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if self.game_state == "BATTLE":
                    self.battle.handle_events(event)

            # Atualização
            if self.game_state == "KITCHEN":
                self.player.update(dt)
            if self.game_state == "BATTLE":
                battle_result = self.battle.update()
                if battle_result:
                    print(f"A batalha acabou com o resultado: {battle_result}")
                    self.game_state = "KITCHEN"
                    self.player.pos = pygame.math.Vector2(self.screen.get_width() * 0.25, self.screen.get_height() * 0.5)
                    self.player.health = self.player.max_health

            # Desenho
            self.screen.fill(settings.BLACK)
            self.all_sprites.draw(self.screen)

            if self.game_state == "BATTLE":
                self.battle.draw(self.screen)

            pygame.display.flip()
            #self.clock.tick(settings.FPS)

if __name__ == "__main__":
    game = Game()
    game.run()