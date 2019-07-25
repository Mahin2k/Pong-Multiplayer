import pygame, sys, time, math, random, os
from pygame.locals import *



# open game window centered on the screen
os.environ['SDL_VIDEO_CENTERED'] = "1"

pygame.init()

#colors, its B&W lol
dark_gray = (25 , 25, 25)
white = (255, 255, 255)
res = (1250, 720)
darker_gray = (15, 15, 15)
black = (0,0,0)
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
        
    def draw(self, x, y):
        self.rect = pygame.draw.rect(display, white, (x, y, 25, 150 ))
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

class update:
    def __init__(self):
        player_one.update()
        player_ai.ai_update(Ball.y)
        Ball.update()
        Ball.score()

    def stop():
        pass



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

small_font = pygame.font.Font('Roboto-Regular.ttf', 25) 
font = pygame.font.Font('Roboto-Regular.ttf', 32) 
largeFont = pygame.font.Font('Roboto-Regular.ttf', 60) 

finished = False

state = 'menu'

class game:

    def __init__(self):
        global state
        
        if state == 'menu':
            player_one.draw(20, 330)
            player_ai.draw(1200, 330)
            background =  pygame.draw.rect(display, darker_gray, (400, 200, 450, 250))
            title = largeFont.render('PONG ONLINE', 1, white, darker_gray )
            question = small_font.render('How would you like to play?', 1, white, darker_gray)
            self.online_txt = font.render('online', 1, white, dark_gray)
            self.offline_txt = font.render('offline', 1, white, dark_gray)

            display.blit(title, (430, 210))
            display.blit(question, (475, 300))
            pygame.draw.rect(display, dark_gray, (510, 390, 100, 55))
        
            self.online_btn = pygame.draw.rect(display, white, (500, 395, 125, 47))
            pygame.draw.rect(display, dark_gray, (505, 400, 115, 38 ))

            self.offline_btn = pygame.draw.rect(display, white, (640, 395, 125, 47))
            pygame.draw.rect(display, dark_gray, (645, 400, 115, 38 ))

            display.blit(self.online_txt, (520, 400))
            display.blit(self.offline_txt, (660, 400))

            if pygame.mouse.get_pressed()[0]:
                mouse_pos = pygame.mouse.get_pos()
                if self.offline_btn.collidepoint(mouse_pos):
                    state = 'offline'
                if self.online_btn.collidepoint(mouse_pos):
                    state = 'online'

        elif state == 'online_waiting': 
            background =  pygame.draw.rect(display, darker_gray, (400, 200, 450, 250))
            waiting_txt = font.render('waiting for player two', 1, dark_gray)
            display.blit(waiting_txt, (430, 210))
            print(state)

    def update(self):
        global state

        if state == 'offline':
            update()
        elif state == 'online':
            self.online()

    def online(self):
            player_one.draw(20, 330)
            player_ai.draw(1200, 330)
            background =  pygame.draw.rect(display, darker_gray, (400, 200, 450, 250))
            title = largeFont.render('PONG ONLINE', 1, white, darker_gray )
            question = small_font.render('How would you like to play?', 1, white, darker_gray)
            self.create_txt = font.render('create', 1, white, dark_gray)
            self.join_txt = font.render('join', 1, white, dark_gray)

            display.blit(title, (430, 210))
            display.blit(question, (475, 300))
            pygame.draw.rect(display, dark_gray, (510, 390, 100, 55))
        
            self.create_btn = pygame.draw.rect(display, white, (500, 395, 125, 47))
            pygame.draw.rect(display, dark_gray, (505, 400, 115, 38 ))

            self.join_btn = pygame.draw.rect(display, white, (640, 395, 125, 47))
            pygame.draw.rect(display, dark_gray, (645, 400, 115, 38 ))

            display.blit(self.create_txt, (520, 400))
            display.blit(self.join_txt, (675, 400))

            if pygame.mouse.get_pressed()[0]:
                mouse_pos = pygame.mouse.get_pos()
                if self.create_btn.collidepoint(mouse_pos):
                    state = 'online_waiting'
                    print(state)
                elif self.join_btn.collidepoint(mouse_pos):
                    state = 'online_join'
                    print(state)



while not finished:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                finished = True
    
    display.fill(dark_gray)
    draw_dashed_line()
    draw_scores()
    check_winner()



    
    #updating objects and screen
    Game = game()
    Game.update()
   
    pygame.display.update()

    
    

pygame.quit()
sys.exit()