import pygame
from game import *
import sys
import os
from constants import *

backgroundPath = "../assets/stages/fireHell.gif"

key_binding_player1 = {
    "up": pygame.K_z,
    "down": pygame.K_s,
    "left": pygame.K_q,
    "right": pygame.K_d,
    "lowKick": pygame.K_u,
    "leftPunch": pygame.K_i
}

key_binding_player2 = {
    "up": pygame.K_UP,
    "down": pygame.K_DOWN,
    "left": pygame.K_LEFT,
    "right": pygame.K_RIGHT,
    "lowKick": pygame.K_p,
    "leftPunch": pygame.K_o
}

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game Menu")

font = pygame.font.Font(None, 36)
button_font = pygame.font.Font(None, 28)

def draw_text(text, font, color, surface, x, y):
    """Function to render text on screen."""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)

def draw_button(surface, text, x, y, width, height, color, highlight=False):
    """Draw a button with optional highlighting."""
    button_rect = pygame.Rect(x - width // 2, y - height // 2, width, height)
    if highlight:
        pygame.draw.rect(surface, (255, 255, 0), button_rect) 
    else:
        pygame.draw.rect(surface, color, button_rect)
    draw_text(text, button_font, (0, 0, 0), surface, x, y)
    return button_rect

def show_main_menu():
    """Display the main menu with options."""
    gradient = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    for i in range(SCREEN_HEIGHT):
        r = 0
        g = min(100 + i // 6, 255)
        b = min(200 + i // 4, 255)
        color = (r, g, b)
        pygame.draw.line(gradient, color, (0, i), (SCREEN_WIDTH, i))

    screen.blit(gradient, (0, 0))
    
    draw_text("Main Menu : Resberry-fight", font, (255, 255, 255), screen, SCREEN_WIDTH // 2, 50)

    start_button = draw_button(screen, "Start Game", SCREEN_WIDTH // 2, 150, 200, 50, (0, 255, 0))
    edit_button = draw_button(screen, "Edit Key Bindings", SCREEN_WIDTH // 2, 250, 200, 50, (0, 255, 0))
    map_button = draw_button(screen, "Choose Map", SCREEN_WIDTH // 2, 350, 200, 50, (0, 255, 0))
    quit_button = draw_button(screen, "Quit Game", SCREEN_WIDTH // 2, 450, 200, 50, (255, 0, 0))

    pygame.display.flip()
    return start_button, edit_button, map_button, quit_button

def show_key_binding_screen():
    """Display the key binding screen for both players."""
    screen.fill((0, 0, 0))  
    draw_text("Edit Key Bindings", font, (255, 255, 255), screen, SCREEN_WIDTH // 2, 50)

    buttons_player1 = {}
    actions_player1 = list(key_binding_player1.keys())
    y_offset = 100
    
    for i, action in enumerate(actions_player1):
        y_pos = y_offset + i * 70
        button_text = pygame.key.name(key_binding_player1[action])
        button = draw_button(screen, button_text, SCREEN_WIDTH // 4 + 150, y_pos, 100, 40, (0, 255, 0))
        buttons_player1[action] = button
        label_text = action.capitalize()
        draw_text(label_text, button_font, (255, 255, 255), screen, SCREEN_WIDTH // 4 - 100, y_pos)

    buttons_player2 = {}
    actions_player2 = list(key_binding_player2.keys())
    
    y_offset = 100
    for i, action in enumerate(actions_player2):
        y_pos = y_offset + i * 70
        button_text = pygame.key.name(key_binding_player2[action])
        button = draw_button(screen, button_text, 3 * SCREEN_WIDTH // 4 + 150, y_pos, 100, 40, (0, 255, 0))
        buttons_player2[action] = button
        label_text = action.capitalize()
        draw_text(label_text, button_font, (255, 255, 255), screen, 3 * SCREEN_WIDTH // 4 - 100, y_pos)

    back_button = draw_button(screen, "Back", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100, 200, 50, (255, 255, 0))

    pygame.display.flip()
    return buttons_player1, buttons_player2, back_button

def change_key_binding(player, action):
    """Wait for the player to press a key to change the binding."""
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                key_binding = key_binding_player1 if player == 1 else key_binding_player2
                key_binding[action] = event.key
                return pygame.key.name(event.key)

def start_game(backgroundPath):
    """Start the game with the chosen background."""
    print(f"Starting game with background: {backgroundPath}")
    game = Game(key_binding_player1, key_binding_player2, backgroundPath)
    game.run()

def choose_map():
    """Allow the user to choose a map."""
    map_folder = "../assets/stages/"
    maps = [file for file in os.listdir(map_folder) if file.endswith(".gif")]

    gradient = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    for i in range(SCREEN_HEIGHT):
        r = 0
        g = min(100 + i // 6, 255)
        b = min(200 + i // 4, 255)
        color = (r, g, b)
        pygame.draw.line(gradient, color, (0, i), (SCREEN_WIDTH, i))

    screen.blit(gradient, (0, 0))
    draw_text("Choose Map", font, (255, 255, 255), screen, SCREEN_WIDTH // 2, 50)

    map_buttons = {}
    max_columns = 3
    map_width = 180
    map_height = 120
    horizontal_spacing = 20
    vertical_spacing = 20
    x_offset = (SCREEN_WIDTH - (max_columns * map_width + (max_columns - 1) * horizontal_spacing)) // 2
    y_offset = 150

    for i, map_name in enumerate(maps):
        map_preview = pygame.image.load(os.path.join(map_folder, map_name))
        map_preview = pygame.transform.scale(map_preview, (map_width, map_height))

        row = i // max_columns
        col = i % max_columns
        screen.blit(map_preview, (x_offset + col * (map_width + horizontal_spacing), y_offset + row * (map_height + vertical_spacing)))

        map_button = draw_button(screen, "", x_offset + col * (map_width + horizontal_spacing) + map_width // 2,
                                 y_offset + row * (map_height + vertical_spacing) + map_height + 20, 100, 40, (0, 255, 0))
        map_buttons[map_name] = map_button

    back_button = draw_button(screen, "Back", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100, 200, 50, (255, 255, 0))

    pygame.display.flip()
    return map_buttons, maps, back_button

def main():
    """Main function to run the menu and handle choices."""
    from game import Game
    running = True
    in_key_binding = False
    in_map_select = False
    global backgroundPath

    while running:
        if not in_key_binding and not in_map_select:
            start_button, edit_button, map_button, quit_button = show_main_menu()
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.collidepoint(event.pos):
                        start_game(backgroundPath)
                        return
                    elif edit_button.collidepoint(event.pos):
                        in_key_binding = True
                    elif map_button.collidepoint(event.pos):
                        in_map_select = True
                    elif quit_button.collidepoint(event.pos):
                        running = False

        elif in_map_select:
            map_buttons, maps, back_button = choose_map()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for map_name, button in map_buttons.items():
                        if button.collidepoint(event.pos):
                            backgroundPath = os.path.join("../assets/stages", map_name)
                            in_map_select = False  # Update backgroundPath and exit map select

                    if back_button.collidepoint(event.pos):
                        in_map_select = False
        
        elif in_key_binding:
            buttons_player1, buttons_player2, back_button = show_key_binding_screen()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for action, button in buttons_player1.items():
                        if button.collidepoint(event.pos):
                            new_key = change_key_binding(1, action)
                            button = draw_button(screen, new_key, SCREEN_WIDTH // 4 + 150, y_pos, 100, 40, (0, 255, 0))

                    for action, button in buttons_player2.items():
                        if button.collidepoint(event.pos):
                            new_key = change_key_binding(2, action)
                            button = draw_button(screen, new_key, SCREEN_WIDTH // 4 + 150, y_pos, 100, 40, (0, 255, 0))

                    if back_button.collidepoint(event.pos):
                        in_key_binding = False

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
