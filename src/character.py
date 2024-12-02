import pygame

class Character:
    def __init__(self, name, x, y):
        self.axeXpos = x
        self.axeYpos = y
        self.health = 100
        self.name = name
        self.state = "standing"

    def forward(self):
        self.axeXpos += 10
    def backward(self):
        self.axeXpos -= 10

    def jump(self):
        if self.state == "standing":  # Only allow jumping from the standing position
            self.state = "jumping"

    def crouch(self):
        if self.state == "standing":  # Only allow crouching from the standing position
            self.state = "crouching"

    def stand(self):
        self.state = "standing"

    def hurt(self, damage):
        self.health = max(0, self.health - damage)

    def draw_health_bar(self, screen, x, y):

        bar_width = 200
        bar_height = 20
        health_ratio = self.health / 100
        current_width = bar_width * health_ratio

        pygame.draw.rect(screen, (100, 100, 100), (x, y, bar_width, bar_height))

        pygame.draw.rect(screen, (0, 255, 0), (x, y, current_width, bar_height))

        pygame.draw.rect(screen, (255, 255, 255), (x, y, bar_width, bar_height), 2)


#def get_hitbox(self)     #To do