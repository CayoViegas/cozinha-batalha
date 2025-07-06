import pygame
import settings

def draw_panel(screen):
    panel_height = settings.SCREEN_HEIGHT // 3
    panel_rect = pygame.Rect(0, settings.SCREEN_HEIGHT - panel_height, settings.SCREEN_WIDTH, panel_height)

    pygame.draw.rect(screen, settings.WHITE, panel_rect)
    pygame.draw.rect(screen, settings.BLACK, panel_rect, 3)


def draw_text(screen, text, size, x, y, color=settings.BLACK):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def draw_health_bar(screen, current_health, max_health, rect):
    ratio = current_health / max_health

    pygame.draw.rect(screen, settings.RED, rect)

    current_width = rect.width * ratio
    current_rect = pygame.Rect(rect.left, rect.top, current_width, rect.height)
    pygame.draw.rect(screen, settings.GREEN, current_rect)

    pygame.draw.rect(screen, settings.WHITE, rect, 2)