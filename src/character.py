import pygame

class Character:
    def __init__(self, name, x, y):
        self.axeXpos = x
        self.axeYpos = y
        self.health = 100
        self.name = name
        self.state = "standing"
        self.width = 50  # Largeur du personnage
        self.height = 100  # Hauteur par défaut
        self.hitbox = pygame.Rect(x, y, self.width, self.height)  # Hitbox

    def forward(self):
        self.axeXpos += 10
        print(f"{self.name} has moved forward")

    def backward(self):
        self.axeXpos -= 10

    def jump(self):
        if self.state == "standing":
            self.state = "jumping"

    def crouch(self):
        if self.state == "standing":
            self.state = "crouching"

    def stand(self):
        self.state = "standing"

    def hurt(self, damage):
        self.health = max(0, self.health - damage)

    def update_hitbox(self):
        """Met à jour la hitbox en fonction de l'état et de la position."""

        if self.state == "crouching":
            self.hitbox.height = 50  # Crouching réduit la hauteur
        
        elif self.state == "jumping":
            self.hitbox.height = 100
        
        self.hitbox.topleft = (self.axeXpos, self.axeYpos)

    def take_hit(self, attack_type):
        """
        Vérifie si un coup atteint le personnage en fonction de son état.
        :param attack_type: "high" pour un coup haut, "low" pour un coup bas.
        """

        if attack_type == "high" and self.state == "crouching":
            print(f"{self.name} esquive un coup haut en étant accroupi!")
            return False  # Coup esquivé
        
        elif attack_type == "low" and self.state == "jumping":
            print(f"{self.name} esquive un coup bas en sautant!")
            return False  # Coup esquivé
        
        else:
            damage = 10  # Exemple de dégâts
            self.hurt(damage)
            print(f"{self.name} reçoit un coup et perd {damage} points de vie.")

            return True  # Coup réussi

    def draw_health_bar(self, screen, x, y):
        bar_width = 200
        bar_height = 20
        health_ratio = self.health / 100
        current_width = bar_width * health_ratio

        pygame.draw.rect(screen, (100, 100, 100), (x, y, bar_width, bar_height))  # Barre de fond
        pygame.draw.rect(screen, (0, 255, 0), (x, y, current_width, bar_height))  # Barre de santé
        pygame.draw.rect(screen, (255, 255, 255), (x, y, bar_width, bar_height), 2)  # Contour

    def draw(self, screen):
        """Dessine le personnage et sa hitbox."""
        
        self.update_hitbox()
        pygame.draw.rect(screen, (255,0,0), self.hitbox, 2)  # Dessine la hitbox (en rouge)