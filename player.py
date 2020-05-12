import pygame

import sys
import pygame
import ball


class Player():
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x,y,width,height)
        self.value = 0.5
        self.shoot = None
        self.left =False
        self.right = False
        self.up = False
        self.down = False

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)
    

    def move(self):
        keys = pygame.key.get_pressed()
        if self.left or self.up:
            direction = -1
        else:
            direction = 1
        if keys[pygame.K_SPACE]:
            self.shoot = ball.Ball(round(self.x + self.width//2),round(self.y + self.height//2),6,(0,0,0), direction )
        if self.shoot is not None: 
            if self.left or self.right:
                if self.shoot.x < 500 and self.shoot.x >0:   
                    self.shoot.x+=self.shoot.value
                else:
                    self.shoot = None
            else:
                if self.shoot.y < 500 and self.shoot.y >0:   
                    self.shoot.y+=self.shoot.value
                else:
                    self.shoot = None         
        if keys[pygame.K_a] and self.x > 0:
            self.x -= self.value
            self.left = True
            self.up = False
            self.right = False
            self.down = False
        if keys[pygame.K_w] and self.y > 0:
            self.y -= self.value
            self.up = True
            self.right = False
            self.down = False
            self.left =False
        if keys[pygame.K_d] and self.x < 450:
            self.x += self.value
            self.right = True
            self.down = False
            self.left =False
            self.up = False
        if keys[pygame.K_s] and self.y < 450:
            self.y += self.value
            self.down = True
            self.left =False
            self.up = False
            self.right = False
        #self.update()