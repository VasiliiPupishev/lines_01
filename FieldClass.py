import random
import pygame
import os
from BallClass import Ball
import random

pygame.init()
screen = pygame.display.set_mode((900, 900))


class Field:
    Width = 9
    Height = 9
    Balls = []
    Score = 0
    BestScore = 0
    Image = pygame.image.load(os.path.join('Materials', 'field.jpg')).convert()
    Next = []

    @staticmethod
    def set_balls(old_balls):
        balls = []
        colors = ["red", "blue", "green", "pink", "bluelite", "yellow", "brown"]
        for i in range(3):
            again = True
            while again:
                x = random.randint(0, 8)
                y = random.randint(0, 8)
                color = random.randint(0, 6)
                flag = False
                for ball in balls:
                    if x == ball.X and y == ball.Y:
                        flag = True
                        break
                for ball in old_balls:
                    if x == ball.X and y == ball.Y:
                        flag = True
                        break
                if flag is False:
                    balls.append(Ball(x, y, colors[color], False))
                    again = False
        for ball in balls:
            s = random.randint(1, 100)
            if s > 90:
                ball.change_live(True)
        return balls

    #аниамация(+) + звуки при дествии(+) + посказки + ии для подсказок + таблица рекордов(+) + сохранение(+) + разные типы шариков (радиус) + супершарики(проходить насквозь)

    def __init__(self, text_file):
        text = open(text_file, 'r')
        self.BestScore = int(text.readlines()[0])
        self.Image = pygame.transform.scale(self.Image, (602, 400))
        self.Balls = self.set_balls(self.Balls)
        self.Next = self.set_balls(self.Balls)

