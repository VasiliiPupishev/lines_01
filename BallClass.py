import os
import pygame

pygame.init()
screen = pygame.display.set_mode((900, 900))


class Ball:
    X = 0
    Y = 0
    Color = ""
    Image = pygame.image.load(os.path.join('Materials', 'default.jpg')).convert_alpha()
    Lives = False

    def __init__(self, x, y, color, lives):
        self.Color = color
        self.Lives = lives
        self.X = x
        self.Y = y
        name = ""
        if color == "red":
            name = "red.png"
        if color == "green":
            name = "green.png"
        if color == "blue":
            name = "blue.png"
        if color == "yellow":
            name = "yellow.png"
        if color == "bluelite":
            name = "bluelite.png"
        if color == "brown":
            name = "brown.png"
        if color == "pink":
            name = "pink.png"
        if color == "default":
            return
        if self.Lives:
            name = "s" + name
        self.Image = pygame.image.load(os.path.join('Materials', name)).convert_alpha()
        self.Image = pygame.transform.scale(self.Image, (35, 35))

    def change_live(self, bul):
        self.Lives = bul
        if bul:
            self.Image = pygame.image.load(os.path.join('Materials', "s" + self.Color + ".png")).convert_alpha()
            self.Image = pygame.transform.scale(self.Image, (35, 35))
