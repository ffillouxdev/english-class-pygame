import pygame
from PIL import Image  # Pillow for GIF handling
from .constants import *
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

        spriteFolder = SPRITE_FOLDER + "Ryu"

        self.key_binding_player1 = {
            "up" : pygame.K_z,
            "down" : pygame.K_s,
            "left" : pygame.K_q,
            "right" : pygame.K_d,
            "lowKick" : pygame.K_u,
            "leftPunch" : pygame.K_i
        }

        self.key_binding_player2 = {
            "up" : pygame.K_UP,
            "down" : pygame.K_DOWN,
            "left" : pygame.K_LEFT,
            "right" : pygame.K_RIGHT,
            "lowKick" : pygame.K_p,
            "leftPunch" : pygame.K_o
        } #maybe create a key binding option in the game itself? (super easy)
        
        #Initialize the 2 players
        self.player1 = Character("Player 1", 100, SCREEN_HEIGHT//2, spriteFolder)
        self.player2 = Character("Player 2", SCREEN_WIDTH * 0.8, SCREEN_HEIGHT//2, spriteFolder)

        # Initialize health bars
        self.player1_health_bar = HealthBar(self.player1, 50, 50, 400, 50)
        self.player2_health_bar = HealthBar(self.player2, SCREEN_WIDTH - 450 , 50, 400, 50)

        # Load GIF frames
        self.gif_frames, self.gif_size = self.load_gif_frames("./assets/stages/fireHell.gif")
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
            else: # to do : look for the winner then annonce it in the main page
                self.counter.reset()
            self.last_counter_update = current_time

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

            #BIG BIG BIG NONSENS DON'T WORRY ! ----------------------------------

            #if the attack touched the player (his hit box then)
            if(player == self.player1):
                if(self.player2.take_hit("low")):
                    self.player2.hurt(0.1)
            if(self.player1.take_hit("low")):
                self.player1.hurt(0.1)


            #----------------------------------------------------------------------
            
        elif action == "leftPunch":
            player.leftPunch()

        player.update_animation()




    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                #this is for the actions that goes once, like punching kicking, jumping, it verify if the key is pressed and then does it one time
                if event.type == pygame.KEYDOWN:
                    for action, input in self.key_binding_player1.items():
                        if event.key == input:
                            self.handle_player_action(self.player1, action)
                    
                    for action, input in self.key_binding_player2.items():
                        if event.key == input:
                            self.handle_player_action(self.player2, action)

            keyPressed = pygame.key.get_pressed() #a list of true or false of all keys (true for : key is pressed; false for : key is not pressed)

            for action, input in self.key_binding_player1.items():
                if keyPressed[input] : #if the key is pressed or not (true while the key is pressed by the way)
                    self.handle_player_action(self.player1,action)

            for action, input in self.key_binding_player2.items():
                if keyPressed[input] :
                    self.handle_player_action(self.player2,action)

            

            # Update GIF frame and counter
            self.update_gif_frame()
            self.update_counter()

            # Draw the background first
            background = self.gif_frames[self.current_frame]
            self.screen.blit(background, (0, 0))

            # Draw characters
            self.player1.update_animation()
            self.player2.update_animation()

            # Determine if Player 2 should flip to face Player 1
            flip_player2 = self.player2.axeXpos > self.player1.axeXpos

            # Draw characters with their animations
            self.player1.draw(self.screen)
            self.player2.draw(self.screen, flip=flip_player2)

            # Draw health bars
            self.player1_health_bar.draw(self.screen)
            self.player2_health_bar.draw(self.screen)

            # Draw hitboxes
            self.player1.draw_hitbox(self.screen)
            self.player2.draw_hitbox(self.screen)

            # Render the counter on screen
            font = pygame.font.Font(None, 74)
            text = font.render(str(self.counter.get_count()), True, (255, 255, 255))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 80))
            self.screen.blit(text, text_rect.topleft)

            # Update the display
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
