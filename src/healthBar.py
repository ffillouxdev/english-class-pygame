import pygame
class HealthBar:
    def __init__(self, character, x, y, width, height):
        self.character = character
        self.x = x 
        self.y = y
        self.width = width  
        self.height = height 

    def draw(self, screen):
        
        pygame.draw.rect(screen, (100, 100, 100), (self.x, self.y, self.width, self.height))

        
        health_ratio = self.character.health / 100
        current_width = self.width * health_ratio
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, current_width, self.height))

        
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height), 2)
