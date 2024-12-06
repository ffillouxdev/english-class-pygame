# src/game.py
import pygame
from PIL import Image  # Pillow pour gérer les GIFs
from .constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from .counter import Counter
from time import sleep
from .character import *
from .healthBar import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Rasberry-Fight")  # le titre
        self.running = True
        self.counter = Counter(99)
        self.clock = pygame.time.Clock()

        self.player1 = Character("Player 1", 200, SCREEN_HEIGHT - 100)
        self.player2 = Character("Player 2", SCREEN_WIDTH - 250, SCREEN_HEIGHT - 100)

        # Initialize health bars
        self.player1_health_bar = HealthBar(self.player1, 50, 50, 200, 20)
        self.player2_health_bar = HealthBar(
            self.player2, SCREEN_WIDTH - 250, 50, 200, 20
        )

        # Charger les frames du GIF
        self.gif_frames, self.gif_size = self.load_gif_frames(
            "./assets/sprites/BackGround.gif"
        )
        self.current_frame = 0  # Frame actuelle
        self.frame_rate = 120  # Vitesse d'animation (10 FPS)
        self.frame_counter = 0  # Compteur pour gérer le défilement des frames

    def load_gif_frames(self, file_path):
        """Charger les frames d'un GIF en utilisant Pillow."""
        gif = Image.open(file_path)
        frames = []
        try:
            while True:
                frame = gif.copy()
                frame_surface = pygame.image.fromstring(
                    frame.tobytes(), frame.size, frame.mode
                )
                frames.append(frame_surface)
                gif.seek(len(frames))  # Aller à la frame suivante
        except EOFError:
            pass  # Fin du GIF
        return frames, gif.size

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Fond d'écran animé
            self.frame_counter += 1
            if self.frame_counter >= FPS // self.frame_rate:
                self.current_frame = (self.current_frame + 1) % len(self.gif_frames)
                self.frame_counter = 0
            background = self.gif_frames[self.current_frame]
            self.screen.blit(background, (0, 0))
x²
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
