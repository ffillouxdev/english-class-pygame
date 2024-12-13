import pygame
import os

class Character:
    def __init__(self, name, x, y, sprite_folder):
        self.axeXpos = x
        self.axeYpos = y
        self.health = 100
        self.name = name
        self.state = "stand"
        self.width = 150  # Width of the character
        self.height = 300  # Default height
        self.hitbox = pygame.Rect(x, y, self.width, self.height)  # Hitbox

        # Only load the idle sprites
        self.sprites = {
            "stand": self.load_sprites(sprite_folder + "/idle/final"),
            "jump" : self.load_sprites(sprite_folder + "/jump/final"),
            "walk" : self.load_sprites(sprite_folder + "/walk/final"),
            "ko": self.load_sprites(sprite_folder + "/ko/final"),
            "leftPunch" : self.load_sprites(sprite_folder + "/leftPunch/final"),
            "lowKick" : self.load_sprites(sprite_folder + "/lowKick/final"),
            "crouch" : self.load_sprites(sprite_folder + "/crouch/final")
        }

        self.current_sprite_list = self.sprites[self.state]
        self.current_index = 0
        self.animation_speed = 13  # Speed of animation frames
        self.animation_counter = 0

    def load_sprites(self, folderPath):
        images = []
        if not os.path.exists(folderPath):
            print(f"ERROR: Folder {folderPath} does not exist!")
            return []

        for file in sorted(os.listdir(folderPath)):
            if file.endswith('.png'):
                try:
                    img = pygame.image.load(os.path.join(folderPath, file)).convert_alpha()
                    images.append(img)
                    print(f"Loaded {file}")
                except pygame.error as e:
                    print(f"Failed to load {file}: {e}")

        if len(images) == 0:
            print(f"No images found in {folderPath}")
        return images



    def update_hitbox(self):
        """Update the hitbox according to the character's position."""
        self.hitbox.topleft = (self.axeXpos, self.axeYpos)

    def draw_hitbox(self, screen):
        """Draw the hitbox on the screen for debugging purposes."""
        self.update_hitbox()
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)

    def draw(self, screen, flip=False):
        """Draw the character and its hitbox."""
        if self.current_sprite_list:
            current_sprite = self.current_sprite_list[self.current_index]

            if flip:
                current_sprite = pygame.transform.flip(current_sprite, True, False)
            
            # Scale the sprite to match the hitbox dimensions
            current_sprite = pygame.transform.scale(current_sprite, (self.hitbox.width, self.hitbox.height))

            screen.blit(current_sprite, (self.axeXpos, self.axeYpos))

        self.update_hitbox()
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)  # Draw the hitbox in red



    def update_animation(self):
        """Update the animation frames."""
        self.animation_counter += 1

        if self.animation_counter >= self.animation_speed:
            self.animation_counter = 0
            self.current_index += 1
            if self.current_index >= len(self.current_sprite_list):
                self.current_index = 0  # Loop back to the first frame
