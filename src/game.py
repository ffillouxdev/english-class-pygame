import pygame
from PIL import Image  # Pillow for GIF handling
from .constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from .counter import Counter
from .character import *
from .healthBar import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Rasberry-Fight")
        self.running = True
        self.counter = Counter(99)
        self.clock = pygame.time.Clock()

        self.player1 = Character("Player 1", 200, SCREEN_HEIGHT - 100)
        self.player2 = Character("Player 2", SCREEN_WIDTH - 250, SCREEN_HEIGHT - 100)

        # Initialize health bars
        self.player1_health_bar = HealthBar(self.player1, 50, 50, 200, 20)
        self.player2_health_bar = HealthBar(self.player2, SCREEN_WIDTH - 250, 50, 200, 20)

        # Load GIF frames
        self.gif_frames, self.gif_size = self.load_gif_frames(
            "./assets/sprites/BackGround.gif"
        )
        self.current_frame = 0
        self.last_frame_update = pygame.time.get_ticks()  # Tracks the last frame update time
        self.frame_delay = 1000 // 10  # GIF frame rate (10 FPS)

        # Counter update timing
        self.last_counter_update = pygame.time.get_ticks()  # Tracks the last counter update time
        self.counter_delay = 1000  # 1-second delay for the counter

    def load_gif_frames(self, file_path):
        """Load frames from a GIF using Pillow."""
        gif = Image.open(file_path)
        frames = []
        try:
            while True:
                # Ensure the frame is in a supported mode
                frame = gif.copy()
                if frame.mode != "RGB":
                    frame = frame.convert("RGB")
                frame_surface = pygame.image.fromstring(
                    frame.tobytes(), frame.size, frame.mode
                )
                frames.append(frame_surface)
                gif.seek(gif.tell() + 1)  # Move to the next frame
        except EOFError:
            pass  # End of GIF
        return frames, gif.size

    def update_gif_frame(self):
        """Update the current GIF frame based on timing."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_frame_update >= self.frame_delay:
            self.current_frame = (self.current_frame + 1) % len(self.gif_frames)
            self.last_frame_update = current_time

    def update_counter(self):
        """Update the counter based on timing."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_counter_update >= self.counter_delay:
            if self.counter.get_count() > 0:
                self.counter.decrement()
            else:
                self.counter.reset()
            self.last_counter_update = current_time

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Update the GIF frame and counter independently
            self.update_gif_frame()
            self.update_counter()

            # Draw the animated background
            background = self.gif_frames[self.current_frame]
            self.screen.blit(background, (0, 0))

            # Display the counter
            font = pygame.font.Font(None, 74)
            text = font.render(str(self.counter.get_count()), True, (255, 255, 255))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 100))
            self.screen.blit(text, text_rect.topleft)

            # Draw health bars
            self.player1_health_bar.draw(self.screen)
            self.player2_health_bar.draw(self.screen)

            # Update the display
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
