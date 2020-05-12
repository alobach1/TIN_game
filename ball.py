import sys
import player
import pygame


class Ball():
    def __init__(self,x, y, radius, color, direction ):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color 
        self.direction = direction
        self.value = 8 * direction

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)