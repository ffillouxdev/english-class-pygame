# src/game.py
import pygame
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Rasberry-Fight")  # le titre
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Fond d'écran (si vous avez une image bg.jpg dans assets/)
            background = pygame.image.load("assets/bg.jpg")
            bg_rect = background.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(background, bg_rect.topleft)

            pygame.display.flip()

        pygame.quit()
