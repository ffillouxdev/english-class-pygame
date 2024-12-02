# src/game.py
import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from counter import Counter
from time import sleep
from character import *
from healthBar import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Rasberry-Fight")  # le titre
        self.running = True
        self.counter = Counter(99)
        self.clock = pygame.time.Clock()  # Initialize the clock


        self.player1 = Character("Player 1", 200, SCREEN_HEIGHT - 100)
        self.player2 = Character("Player 2", SCREEN_WIDTH - 250, SCREEN_HEIGHT - 100)

        # Initialize health bars
        self.player1_health_bar = HealthBar(self.player1, 50, 50, 200, 20)  # Top-left
        self.player2_health_bar = HealthBar(self.player2, SCREEN_WIDTH - 250, 50, 200, 20)  # Top-right

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Fond d'écran (si vous avez une image bg.jpg dans assets/)
            background = pygame.image.load("assets/bg.jpg")
            bg_rect = background.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(background, bg_rect.topleft)
            
            # placer le compteur en haut au milieu et le lancer jusqu'à 0
            font = pygame.font.Font(None, 74)
            text = font.render(str(self.counter.get_count()), True, (255, 255, 255))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 100))
            self.screen.blit(text, text_rect.topleft)
            if self.counter.get_count() > 0:
                sleep(1)
                self.counter.decrement()
            else:
                self.counter.reset()

            # Draw health bars
            self.player1_health_bar.draw(self.screen)
            self.player2_health_bar.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(FPS) 

        pygame.quit()

Game = Game()
Game.run()