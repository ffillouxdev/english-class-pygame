# Define constants for movement and actions
FORWARD_SPEED = 10
BACKWARD_SPEED = 10
JUMP_HEIGHT = 10
CROUCH_HEIGHT = 10

from character import Character
import pygame

class Action:
    def __init__(self, character: Character, action):
        self.char = character
        self.action = action
    
    def keyHandling(self):
        if self.action == "up":
            self.jump()
        elif self.action == "down":
            self.crouch()
        elif self.action == "left":
            self.forward()
        elif self.action == "right":
            self.backward()

    def forward(self):
        self.char.axeXpos += FORWARD_SPEED
        self.char.state = ""
        print(f"{self.char.name} has moved forward")

    def backward(self):
        self.char.axeXpos -= BACKWARD_SPEED
        print(f"{self.char.name} has moved backward")

    def jump(self):
        if self.char.state != "jumping":  # Prevent repeated jumps
            self.char.state = "jumping"
            self.char.update_hitbox()
            self.char.axeYpos -= JUMP_HEIGHT  # In most 2D games, Y decreases upwards
            print(f"{self.char.name} jumps!")

    def crouch(self):
        if self.char.state != "crouching":  # Prevent repeated crouch states
            self.char.state = "crouching"
            self.char.update_hitbox()
            self.char.axeYpos += CROUCH_HEIGHT
            print(f"{self.char.name} crouches!")

    def stand(self):
        if self.char.state == "crouching":
            self.char.axeYpos -= CROUCH_HEIGHT
        elif self.char.state == "jumping":
            self.char.axeYpos += JUMP_HEIGHT
        self.char.state = "standing"
        self.char.update_hitbox()

        print(f"{self.char.name} stands up")

    def hurt(self, damage):
        self.char.health -= damage
        print(f"{self.char.name} took {damage} damage")

    def take_hit(self, attack_type):
        """
        Handles logic for the character receiving an attack.
        :param attack_type: "high" for a high attack, "low" for a low attack.
        :return: True if the hit lands, False if it is dodged.
        """
        if attack_type == "high" and self.char.state == "crouching":
            print(f"{self.char.name} dodged a high attack by crouching!")
            return False  # Hit missed
        elif attack_type == "low" and self.char.state == "jumping":
            print(f"{self.char.name} dodged a low attack by jumping!")
            return False  # Hit missed
        else:
            print(f"{self.char.name} got hit!")
            return True  # Hit lands

        