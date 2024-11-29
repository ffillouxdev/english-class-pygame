import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

pygame.init()

# Définir les dimensions de l'écran
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Rasberry-Fight") # le titre

running = True
while running:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Fermer la fenêtre
            running = False

    # background image
    background = pygame.image.load('assets/bg.jpg')
    
    # Rafraîchir l'écran
    pygame.display.flip()

# Quitter Pygame
pygame.quit()
