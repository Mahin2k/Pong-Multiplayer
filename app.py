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



class ball:

    def __init__(self):
        self.direction = 0
        self.speed = 1
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
        elif self.y >= 720:
            self.direction = 180-self.direction

    def score(self):
        if self.x > 1250:
            player_one.score = str(int(player_one.score) + 1).zfill(2)
            self.reset()
        elif self.x < 0 :
            player_ai.score = str(int(player_ai.score )+ 1).zfill(2)
            self.reset()





class paddle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.draw.rect(display, white, (x, y, 25, 150 ))
        
    def ai_update(self, ball_y_pos):
        self.rect = pygame.draw.rect(display, white, (self.x, ball_y_pos-150, 25, 150 ))
        

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

player_one.score = '00'
player_ai.score = '00'

font = pygame.font.Font('Roboto-Medium.ttf', 32) 
largeFont = pygame.font.Font('Roboto-Medium.ttf', 60) 
while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    

    display.fill(dark_gray)
    draw_dashed_line()

    player_one_score = font.render(str(player_one.score), True, white,  dark_gray) 
    player_ai_score = font.render(str(player_ai.score), True, white,  dark_gray) 

    display.blit(player_one_score, (560, 10))
    display.blit(player_ai_score, (650, 10))

    if int(player_ai.score) == 5:
        winner_text = largeFont.render('The winner is: ai', True, white, dark_gray)
        display.blit(winner_text, (400, 270))
    elif int(player_ai.score ) == 6:
        pygame.quit()
        sys.exit()

    if int(player_one.score) == 5:
        winner_text = largeFont.render('The winner is: player one', True, white, dark_gray)
        display.blit(winner_text, (400, 270))
    elif int(player_one.score ) == 6:
        pygame.quit()
        sys.exit()
        
        

    player_one.update()
    player_ai.ai_update(Ball.y)
    Ball.update()
    Ball.score()
    pygame.display.update()