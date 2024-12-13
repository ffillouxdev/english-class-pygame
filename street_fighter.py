import pygame
import sys

# Initialisation
pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Street Fighter - Mini Game")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)





# FPS
clock = pygame.time.Clock()
FPS = 60

# Classes
class Fighter:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, 50, 100)
        self.color = color
        self.health = 100
        self.velocity = 5
        self.punching = False

    def move(self, keys, left, right, up):
        if keys[left]:
            self.rect.x -= self.velocity
        if keys[right]:
            self.rect.x += self.velocity
        if keys[up]:
            self.rect.y -= self.velocity  # Saut basique
            self.rect.y += self.velocity  # Retour au sol

    def attack(self, other):
        if self.punching and self.rect.colliderect(other.rect):
            other.health -= 1

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        # Barre de santé
        pygame.draw.rect(screen, RED, (self.rect.x, self.rect.y - 10, 100, 5))
        pygame.draw.rect(screen, GREEN, (self.rect.x, self.rect.y - 10, self.health, 5))

# Initialisation des combattants
fighter1 = Fighter(100, HEIGHT - 120, RED)
fighter2 = Fighter(600, HEIGHT - 120, BLUE)

# Boucle principale
running = True
while running:
    screen.fill(WHITE)

    # Événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Touches
    keys = pygame.key.get_pressed()

    # Déplacements du joueur 1
    fighter1.move(keys, pygame.K_a, pygame.K_d, pygame.K_w)
    fighter1.punching = keys[pygame.K_SPACE]

    # Déplacements du joueur 2
    fighter2.move(keys, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP)
    fighter2.punching = keys[pygame.K_RETURN]

    # Attaques
    fighter1.attack(fighter2)
    fighter2.attack(fighter1)

    # Dessin des combattants
    fighter1.draw(screen)
    fighter2.draw(screen)

    # Condition de victoire
    if fighter1.health <= 0:
        print("Fighter 2 Wins!")
        running = False
    if fighter2.health <= 0:
        print("Fighter 1 Wins!")
        running = False

    # Mise à jour de l'écran
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
