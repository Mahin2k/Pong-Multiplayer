import pygame
import sys
import time
from pygame.locals import *
import math
import random



pygame.init()

#colors, its B&W lol
dark_gray = (25 , 25, 25)
white = (255, 255, 255)
res = (1250, 720)


#set window size and title
display = pygame.display.set_mode(res)
pygame.display.set_caption("Pong by @stoozy")


player_one_score = str(00)
player_ai_score = str(00)

font = pygame.font.Font('Roboto-Medium.ttf', 32) 
  
# create a text suface object, 
# on which text is drawn on it. 


class ball:

    def __init__(self):
        self.direction = 0
        self.speed = 0.7
        self.reset()  

    def reset(self):
        self.x = 550
        self.y = random.randint(25, 600)
        self.direction = random.randrange(30,45)

        # Flip a 'coin'
        if random.randrange(2) == 0 :
            # Reverse ball direction, let the other guy get it first
            self.direction += 180

    def update(self):
        direction_rad = math.radians(self.direction)
        self.x += self.speed * math.sin(direction_rad)
        self.y -= self.speed * math.cos(direction_rad)
        self.rect = pygame.draw.rect(display, white, (self.x, self.y, 20, 20))
        
        if pygame.sprite.collide_rect(self, player_ai):
            self.direction = 360-self.direction

        if pygame.sprite.collide_rect(self, player_one):
            self.direction = 360-self.direction

        if self.y <= 0:
            self.direction = 180-self.direction
            print('under 0')
        elif self.y >= 720:
            self.direction = 180-self.direction
            print('over 720')

        if self.x > 1250:
            self.reset()
            print('game')
        elif self.x < 0 :
            self.reset()
            print('game')






class paddle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.draw.rect(display, white, (x, y, 25, 150 ))
        
    def ai_update(self, ball_y_pos):
        self.rect =pygame.draw.rect(display, white, (self.x, ball_y_pos, 25, 150 ))
        

    def update(self):
        #pressed keys object. Updates on the while loop
        keys = pygame.key.get_pressed()
        #Player movement 
        if keys[pygame.K_UP]:
            if self.y == 10:
                self.y = self.y
            else:
                self.y -= 0.5
        elif keys[pygame.K_DOWN]:
            if self.y == 560:
                self.y = self.y
            else:
                self.y += 0.5
        self.rect = pygame.draw.rect(display, white, (self.x, self.y, 25, 150 ))



def draw_dashed_line():
    pygame.draw.rect(display, white, (610, 000, 15, 50))
    pygame.draw.rect(display, white, (610, 100, 15, 50))
    pygame.draw.rect(display, white, (610, 200, 15, 50))
    pygame.draw.rect(display, white, (610, 300, 15, 50))
    pygame.draw.rect(display, white, (610, 400, 15, 50))
    pygame.draw.rect(display, white, (610, 500, 15, 50))
    pygame.draw.rect(display, white, (610, 600, 15, 50))
    pygame.draw.rect(display, white, (610, 700, 15, 50))



player_one = paddle(20, 330)
player_ai = paddle(1200, 330)
Ball = ball()

while True:
    text = font.render(player_one_score, True, white,  dark_gray) 
    text_rect = text.get_rect()
    display.blit(text, text_rect)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()


    display.fill(dark_gray)
    draw_dashed_line()



    player_one.update()
    player_ai.ai_update(Ball.y)
    Ball.update()
    pygame.display.update()