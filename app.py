import pygame, sys, time, math, random, os
from pygame.locals import *



# open game window centered on the screen
os.environ['SDL_VIDEO_CENTERED'] = "1"

pygame.init()

#colors, its B&W lol
dark_gray = (25 , 25, 25)
white = (255, 255, 255)
res = (1250, 720)


#set window size and title
display = pygame.display.set_mode(res)
pygame.display.set_caption("Pong by @stoozy")


# this is the ball class. It has a reset and update function. It also keeps track of the score.
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
            # Reverse ball direction
            self.direction += 180

    def update(self):
        direction_rad = math.radians(self.direction)
        self.x += self.speed * math.sin(direction_rad)
        self.y -= self.speed * math.cos(direction_rad)
        #update collisions
        self.collisions()
        
        
    def collisions(self):
        # making the ball a rect object so I can check for collisions
        self.rect = pygame.draw.rect(display, white, (self.x, self.y, 20, 20))
        
        # checking for collisions
        if pygame.sprite.collide_rect(self, player_ai):
            self.direction = 360-self.direction

        if pygame.sprite.collide_rect(self, player_one):
            self.direction = 360-self.direction

        # checking for out of bounds
        if self.y <= 0:
            self.direction = 180-self.direction
        elif self.y >= 720:
            self.direction = 180-self.direction

    def score(self):
        # defining who gets the score
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
        self.rect = pygame.draw.rect(display, white, (x, y, 25, 200 ))
    
    # ai updates differently
    def ai_update(self, ball_y_pos):
        self.y = ball_y_pos
        if ball_y_pos < 10:
            self.y = 10
        if ball_y_pos > 560:
            self.y = 560
        self.rect = pygame.draw.rect(display, white, (self.x, self.y , 25, 150 ))
        

    def update(self):
        #pressed keys object. Updates on the while loop
        keys = pygame.key.get_pressed()
        #Player movement 
        if keys[pygame.K_UP]:
            if self.y == 10:
                self.y = self.y
            else:
                self.y -= 1
        elif keys[pygame.K_DOWN]:
            if self.y == 560:
                self.y = self.y
            else:
                self.y += 1
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

def check_winner():
    if int(player_ai.score) == 5:
        winner_text = largeFont.render('The winner is: computer', True, white, dark_gray)
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

def draw_scores():
    player_one_score = font.render(str(player_one.score), True, white,  dark_gray) 
    player_ai_score = font.render(str(player_ai.score), True, white,  dark_gray) 

    display.blit(player_one_score, (560, 10))
    display.blit(player_ai_score, (650, 10))

player_one = paddle(20, 330)
player_ai = paddle(1200, 330)
Ball = ball()

player_one.score = '00'
player_ai.score = '00'

font = pygame.font.Font('Roboto-Medium.ttf', 32) 
largeFont = pygame.font.Font('Roboto-Medium.ttf', 60) 

finished = False
while not finished:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                finished = True
        if event.type == MOUSEBUTTONDOWN:
            os.putenv('SDL_VIDEO_WINDOW_POS',"100, 100") 
            
    
    display.fill(dark_gray)
    draw_dashed_line()
    draw_scores()
    check_winner()



        
    #updating objects and screen
    player_one.update()
    player_ai.ai_update(Ball.y)
    Ball.update()
    Ball.score()
    pygame.display.update()
    
    

pygame.quit()
sys.exit()