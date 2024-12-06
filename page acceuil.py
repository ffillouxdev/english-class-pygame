import os
import pygame
import sys
from PIL import Image

# Charger le GIF et extraire les frames avec Pillow
def load_gif_frames(file_path):
    gif = Image.open(file_path)
    frames = []
    try:
        while True:
            frame = gif.copy()
            frames.append(pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode))
            gif.seek(len(frames))  # Aller à la frame suivante
    except EOFError:
        pass  # Fin du GIF
    return frames, gif.size

# Initialisation de Pygame
pygame.init()

# Charger le GIF animé
frames, gif_size = load_gif_frames("C:/Users/bille/OneDrive/Documents/projet anglais/fond.gif")
ORIGINAL_WIDTH, ORIGINAL_HEIGHT = gif_size

# Définir la taille de l'écran (dézoom)
ZOOM_FACTOR = 0.8  # Facteur de réduction
WIDTH = int(ORIGINAL_WIDTH * ZOOM_FACTOR)
HEIGHT = int(ORIGINAL_HEIGHT * ZOOM_FACTOR)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Raspberry Fight")

# Redimensionner les frames du GIF pour correspondre au dézoom
frames = [pygame.transform.scale(frame, (WIDTH, HEIGHT)) for frame in frames]

# Animation
frame_index = 0
frame_duration = 100  # Durée en millisecondes pour chaque frame
clock = pygame.time.Clock()

# Police pour les textes
pygame.font.init()
title_font = pygame.font.Font(None, 80)  # Réduction supplémentaire pour le titre
button_font = pygame.font.Font(None, 80)  # Police pour le bouton
info_font = pygame.font.Font(None, 50)  # Police pour le texte explicatif

# Variables pour les animations
title_scale = 0.95  # Point de départ légèrement réduit
title_scale_direction = 1
button_alpha = 255
button_alpha_direction = -10
info_alpha = 0
info_alpha_direction = 5

# Fonction pour passer à la prochaine page
def new_page():
    pygame.quit()  # Ferme la fenêtre actuelle
    os.system(r'python "C:\Users\bille\OneDrive\Documents\english-class-pygame\src\game.py"')# Exécute le fichier street_fighter.py
    sys.exit()

# Définir le bouton START
start_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 50, 300, 80)

# Boucle principale
running = True
while running:
    # Gérer les événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # Vérifie si Entrée est pressé
                new_page()

    # Animation du titre (zoom réduit)
    title_scale += 0.003 * title_scale_direction
    if title_scale > 1.0 or title_scale < 0.9:
        title_scale_direction *= -1

    # Animation du bouton (transparence)
    button_alpha += button_alpha_direction
    if button_alpha > 255:
        button_alpha = 255
        button_alpha_direction *= -1
    elif button_alpha < 50:
        button_alpha = 50
        button_alpha_direction *= -1

    # Animation du texte explicatif (apparaît progressivement)
    info_alpha += info_alpha_direction
    if info_alpha > 255:
        info_alpha = 255

    # Afficher le GIF animé
    screen.blit(frames[frame_index], (0, 0))
    frame_index = (frame_index + 1) % len(frames)  # Passer à la frame suivante

    # Dessiner le titre "Raspberry Fight"
    title_surface = title_font.render("Raspberry Fight", True, (255, 102, 178))  # Rose vif
    title_scaled_surface = pygame.transform.scale(
        title_surface, (int(title_surface.get_width() * title_scale), int(title_surface.get_height() * title_scale))
    )
    screen.blit(title_scaled_surface, (WIDTH // 2 - title_scaled_surface.get_width() // 2, 20))  # Position ajustée

    # Ajouter un fond semi-transparent derrière le bouton
    button_surface = pygame.Surface((start_button.width, start_button.height), pygame.SRCALPHA)  # Surface avec canal alpha
    button_surface.fill((255, 0, 0, button_alpha))  # Rouge avec transparence
    screen.blit(button_surface, (start_button.x, start_button.y))

    # Dessiner le bouton START
    start_text = button_font.render("START", True, (255, 255, 255))  # Texte blanc
    screen.blit(
        start_text,
        (
            start_button.x + start_button.width // 2 - start_text.get_width() // 2,
            start_button.y + start_button.height // 2 - start_text.get_height() // 2,
        ),
    )

    # Dessiner le texte "Press Enter" avec animation de transparence
    info_surface = info_font.render("Press Enter", True, (255, 255, 255))  # Blanc
    info_surface.set_alpha(info_alpha)
    screen.blit(info_surface, (WIDTH // 2 - info_surface.get_width() // 2, start_button.y + 100))

    # Mettre à jour l'écran
    pygame.display.flip()
    clock.tick(1000 // frame_duration)

pygame.quit()
sys.exit()
