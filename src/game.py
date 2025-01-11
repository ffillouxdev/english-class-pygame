import pygame
from PIL import Image
from constants import *
from counter import Counter
from character import *
from healthBar import *
from main import *

def draw_button(screen, text, x, y, width, height, color):
    """Draw a button on the screen."""
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, color, button_rect)

    font = pygame.font.Font(None, 36)
    button_text = font.render(text, True, (0, 0, 0))
    text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, text_rect)

    return button_rect

class Game:
    def __init__(self, key1, key2,backgroundPath):

        pygame.init()
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        pygame.display.set_caption("Rasberry-Fight")
        
        self.running = True
        self.counter = Counter(99)
        self.clock = pygame.time.Clock()

        spriteFolder = SPRITE_FOLDER + "Ryu"

        self.key_binding_player1 = key1

        self.key_binding_player2 = key2

        #Initialize the 2 players
        self.player1 = Character("Player 1", 100, SCREEN_HEIGHT//2, spriteFolder)
        self.player2 = Character("Player 2", SCREEN_WIDTH * 0.8, SCREEN_HEIGHT//2, spriteFolder)

        # Initialize health bars
        self.player1_health_bar = HealthBar(self.player1, 50, 50, 400, 50)
        self.player2_health_bar = HealthBar(self.player2, SCREEN_WIDTH - 450 , 50, 400, 50)

        # Load GIF frames
        self.gif_frames, self.gif_size = self.load_gif_frames(backgroundPath)
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
                frame = gif.copy()

                if frame.mode != "RGB":
                    frame = frame.convert("RGB")

                # Scale the frame to fit the screen size
                frame = frame.resize((SCREEN_WIDTH, SCREEN_HEIGHT), Image.Resampling.LANCZOS)
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
            else: # to do : look for the winner then annonce it in the main page : DONE
                self.counter.reset()
            self.last_counter_update = current_time

    def check_collision(hitbox1, hitbox2):
        """Check if two hitboxes are colliding."""
        return hitbox1.colliderect(hitbox2)


    def handle_player_action(self, player: Character, action):
        """Handles actions for a player based on the keybinding action."""
        if action == "up":
            player.jump()
        elif action == "down":
            player.crouch()
        elif action == "left":
            player.backward()
        elif action == "right":
            player.forward()
        elif action == "lowKick":
            player.lowKick()
        elif action == "leftPunch":
            player.leftPunch()

        player.update_animation()

        # Check for collision after the attack is executed
        if action in ["lowKick", "leftPunch"]:  # Check for attacks only
            if player == self.player1:
                # Corrected collision check for player 1 attacking player 2
                if self.player1.hitbox.colliderect(self.player2.hitbox):
                    self.player2.take_damage(self.player1.attack_damage)
            elif player == self.player2:
                # Corrected collision check for player 2 attacking player 1
                if self.player2.hitbox.colliderect(self.player1.hitbox):
                    self.player1.take_damage(self.player2.attack_damage)


    
    def update_counter(self):
        """Update the counter based on timing."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_counter_update >= self.counter_delay:
            if self.counter.get_count() > 0:
                self.counter.decrement()
            else:  # Time is over
                self.counter.reset()
                self.declare_winner()  # Declare the winner when the time runs out
            self.last_counter_update = current_time

    def check_game_over(self):
        """Check if either player's health is zero."""
        if self.player1.health <= 0:
            self.declare_winner("Player 2")  # Player 2 wins when Player 1 dies
        elif self.player2.health <= 0:
            self.declare_winner("Player 1")  # Player 1 wins when Player 2 dies



    
    def declare_winner(self, winner=None):
        """Announce the winner and display rematch, main menu, and quit buttons."""
        font = pygame.font.Font(None, 74)
        if winner is None:  # If no player died, compare health
            if self.player1.health > self.player2.health:
                winner = "Player 1"
            elif self.player2.health > self.player1.health:
                winner = "Player 2"
            else:
                winner = "Draw"

        # Display the winner on the screen
        winner_text = font.render(f"{winner} Wins!", True, (255, 255, 255))
        winner_rect = winner_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        self.screen.blit(winner_text, winner_rect)

        # Draw "Rematch", "Main Menu", and "Quit" buttons
        rematch_button = draw_button(self.screen, "Rematch", SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 50, 150, 50, (0, 255, 0))
        main_menu_button = draw_button(self.screen, "Main Menu", SCREEN_WIDTH // 2 + 20, SCREEN_HEIGHT // 2 + 50, 150, 50, (255, 255, 0))
        quit_button = draw_button(self.screen, "Quit", SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 + 120, 150, 50, (255, 0, 0))  # New button

        pygame.display.flip()

        # Handle button clicks
        buttons = {"rematch": rematch_button, "main_menu": main_menu_button, "quit": quit_button}
        return buttons

    def handle_end_game_buttons(self, buttons):
        """Handle the clicks on the end game buttons."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Check for "Rematch" button click
                if buttons["rematch"].collidepoint(mouse_pos):
                    self.reset_game()  # Call method to reset game (see below)
                # Check for "Main Menu" button click
                elif buttons["main_menu"].collidepoint(mouse_pos):
                    self.return_to_main_menu()  # Method to return to main menu
                # Check for "Quit" button click
                elif buttons["quit"].collidepoint(mouse_pos):
                    self.quit_game()  # Call the method to quit the game
    

    def reset_game(self):
        """Reset the game for a rematch."""
        self.player1.health = 100
        self.player2.health = 100
        self.counter.reset()
        self.running = True
        start_game(backgroundPath)  # Call the main game loop again

    def return_to_main_menu(self):
        """Return to the main menu after a game is over."""
        self.running = False
        # Call the method to return to the main menu here
        main()

    def quit_game(self):
        """Exit the game."""
        self.running = False
        pygame.quit()
        quit()



    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    for action, input in self.key_binding_player1.items():
                        if event.key == input:
                            self.handle_player_action(self.player1, action)

                    for action, input in self.key_binding_player2.items():
                        if event.key == input:
                            self.handle_player_action(self.player2, action)

            keyPressed = pygame.key.get_pressed()

            for action, input in self.key_binding_player1.items():
                if keyPressed[input]:
                    self.handle_player_action(self.player1, action)

            for action, input in self.key_binding_player2.items():
                if keyPressed[input]:
                    self.handle_player_action(self.player2, action)

            # Update GIF frame and counter
            self.update_gif_frame()
            self.update_counter()

            # Check if the game is over (either time or health)
            self.check_game_over()

            if self.player1.health <= 0 or self.player2.health <= 0 or self.counter.get_count() <= 0:
                # The game is over, show the winner screen
                buttons = self.declare_winner()
                self.handle_end_game_buttons(buttons)  # Handle clicks on the buttons
                continue  # Skip drawing game elements and just show the winner screen

            # Draw the background first
            background = self.gif_frames[self.current_frame]
            self.screen.blit(background, (0, 0))

            # Draw characters
            self.player1.update_animation()
            self.player2.update_animation()

            # Draw characters with their animations
            self.player1.draw(self.screen)
            self.player2.draw(self.screen, flip=self.player2.axeXpos > self.player1.axeXpos)

            # Draw health bars
            self.player1_health_bar.draw(self.screen)
            self.player2_health_bar.draw(self.screen)

            # Render the counter on screen
            font = pygame.font.Font(None, 74)
            text = font.render(str(self.counter.get_count()), True, (255, 255, 255))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 80))
            self.screen.blit(text, text_rect.topleft)

            # Update the display
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()

