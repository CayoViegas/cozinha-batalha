import pygame
import sys
import settings
from src.player import Player
from src.boss import Boss
from src.battle import Battle

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption("Cozinha de Batalha")
        self.clock = pygame.time.Clock()

        self.game_state = "BATTLE"

        self.all_sprites = pygame.sprite.Group()
        self.player = Player((self.screen.get_width() * 0.25, self.screen.get_height() * 0.5), self.all_sprites)
        self.boss = Boss((self.screen.get_width() * 0.75, self.screen.get_height() * 0.5), self.all_sprites)

        self.battle = Battle(self.player, self.boss)

    def run(self):
        while True:
            # Tratamento de eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if self.game_state == "BATTLE":
                    self.battle.handle_events(event)

            # Atualização
            if self.game_state == "BATTLE":
                battle_result = self.battle.update()

                if battle_result:
                    print(f"A batalha terminou com o resultado: {battle_result}")
                    self.game_state = "BATTLE_OVER"

            # Desenho
            self.screen.fill(settings.BLACK)
            self.all_sprites.draw(self.screen)

            if self.game_state == "BATTLE" or self.game_state == "BATTLE_OVER":
                self.battle.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(settings.FPS)

if __name__ == "__main__":
    game = Game()
    game.run()