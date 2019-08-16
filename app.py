import pygame
import sys
import math
import random
import os
from pygame.locals import *
from requests import get
from network import Network


ip = get('https://api.ipify.org').text
state = 'menu'
n = None
is_player_two = False
enemy = None
scores = []
player_one = None
display = None
finished = True
username = ''
winner = ''
# open game window centered on the screen
os.environ['SDL_VIDEO_CENTERED'] = "1"

pygame.init()

clock = pygame.time.Clock()
#   colors, its B&W
dark_gray = (25, 25, 25)
white = (255, 255, 255)
res = (1250, 720)
darker_gray = (15, 15, 15)
black = (0, 0, 0)

pygame.display.set_caption("Pong by @stoozy")


# this is the ball class. It has a reset and update function.
class Ball:

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
            # Reverse ball direction
            self.direction += 180

    def update(self):
        direction_rad = math.radians(self.direction)
        self.x += self.speed * math.sin(direction_rad)
        self.y -= self.speed * math.cos(direction_rad)

        #   update collisions
        self.collisions()

    def online_update(self, x, y):
        # print(x, y)
        self.x = float(x)
        self.y = float(y)
        self.collisions()

    def collisions(self):

        # making the ball a rect object so I can check for collisions
        self.rect = pygame.draw.rect(display, white, (self.x, self.y, 20, 20))

        # checking for collisions
        if state == 'offline':
            if pygame.sprite.collide_rect(self, ai):
                self.direction = 360-self.direction
            if pygame.sprite.collide_rect(self, player):
                self.direction = 360-self.direction

        if state == 'online_game':
            if pygame.sprite.collide_rect(self, enemy):
                self.direction = 360-self.direction
            if pygame.sprite.collide_rect(self, player):
                self.direction = 360-self.direction

        # checking for out of bounds
        if self.y <= 0:
            self.direction = 180-self.direction
        elif self.y >= 720:
            self.direction = 180-self.direction


class Paddle:
    def __init__(self, x, y):
        self.score = '00'
        self.x = x
        self.y = y
        if not display:
            pass
        else:
            self.rect = pygame.draw.rect(display, white, (int(x), int(y), 25, 150))

    def ai_update(self, ball_y_pos):
        self.y = ball_y_pos
        if ball_y_pos < 10:
            self.y = 10
        if ball_y_pos > 560:
            self.y = 560
        self.rect = pygame.draw.rect(display, white, (self.x, self.y, 25, 150))

    def update(self):
        #   pressed keys object. Updates on the while loop
        keys = pygame.key.get_pressed()
        #   Player movement

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
        self.rect = pygame.draw.rect(display, white, (self.x, self.y, 25, 150))

    def online_update(self, x, y):
        self.x = int(x)
        self.y = int(y)
        self.rect = pygame.draw.rect(display, white, (self.x, self.y, 25, 150))


# initializing classes
player = None
ai = Paddle(1200, 330)
ball = Ball()

# fonts for pygame
small_font = pygame.font.Font('Roboto-Regular.ttf', 25)
font = pygame.font.Font('Roboto-Regular.ttf', 32)
largeFont = pygame.font.Font('Roboto-Regular.ttf', 60)


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
    if state == 'offline':
        if int(ai.score) == 5:
            winner_text = largeFont.render('The winner is: computer', True, white, dark_gray)
            display.blit(winner_text, (465, 270))
        elif int(ai.score) == 6:
            pygame.quit()
            sys.exit()
        if int(player.score) == 5:
            winner_text = largeFont.render('The winner is: player one', True, white, dark_gray)
            display.blit(winner_text, (465, 270))
        elif int(player.score) == 6:
            pygame.quit()
            sys.exit()
    elif state == 'online_game':
        # fix for a bug where network receives too much info
        if len(enemy.score) > 2:
            enemy.score = enemy.score[:2]
        if len(player.score) > 2:
            enemy.score = enemy.score[:2]
        if is_player_two:
            if int(enemy.score) == 5:
                winner_text = largeFont.render('You Won!', True, white, dark_gray)
                display.blit(winner_text, (465, 270))
            elif int(enemy.score) == 6:
                pygame.quit()
                sys.exit()
            if int(player.score) == 5:
                winner_text = largeFont.render('You Lost!', True, white, dark_gray)
                display.blit(winner_text, (465, 270))
            elif int(player.score) == 6:
                pygame.quit()
                sys.exit()
        else:
            if int(enemy.score) == 5:
                winner_text = largeFont.render('You Lost!', True, white, dark_gray)
                display.blit(winner_text, (465, 270))
            elif int(enemy.score) == 6:
                pygame.quit()
                sys.exit()
            if int(player.score) == 5:
                winner_text = largeFont.render('You Won!', True, white, dark_gray)
                display.blit(winner_text, (465, 270))
            elif int(player.score) == 6:
                pygame.quit()
                sys.exit()


def draw_scores():
    global player, enemy, scores
    if state == 'online_game':
        # defining who gets the score
        if not is_player_two:
            if ball.x > 1250:
                player.score = str(int(player.score) + 1)
                ball.reset()
            elif ball.x < 0:
                enemy.score = str(int(enemy.score) + 1)
                ball.reset()

            scores = [player.score, enemy.score]

            es = str(enemy.score).zfill(2)
            ps = str(player.score).zfill(2)

            player_score = font.render(str(ps), True, white, dark_gray)
            enemy_score = font.render(str(es), True, white, dark_gray)

            display.blit(player_score, (560, 10))
            display.blit(enemy_score, (650, 10))

        elif is_player_two:
            print(player.score, enemy.score)

            enemy_score = str(enemy.score).zfill(2)
            player_score = str(player.score).zfill(2)

            player_score = font.render(str(player_score), True, white, dark_gray)
            enemy_score = font.render(str(enemy_score), True, white, dark_gray)

            display.blit(player_score, (560, 10))
            display.blit(enemy_score, (650, 10))

    elif state == 'offline':
        if ball.x > 1250:
            player.score = str(int(player.score) + 1).zfill(2)
            ball.reset()
        elif ball.x < 0:
            ai.score = str(int(ai.score) + 1).zfill(2)
            ball.reset()

        player_score = font.render(str(player.score), True, white, dark_gray)
        ai_score = font.render(str(ai.score), True, white, dark_gray)

        display.blit(player_score, (560, 10))
        display.blit(ai_score, (650, 10))


def handle_network():
    global is_player_two, enemy, scores, player, winner
    data = n.rcv(4096)
    if ':' in data:
        if 'player' or 'enemy' in data:
            if 'player' in data:
                winner = 'player'
            elif 'enemy' in data:
                winner = 'enemy'

        arr = data.split(':')

        # update enemy player
        x, y = arr[0].split('.')[1], arr[0].split('.')[2]
        enemy.online_update(x, y)

        # update ball position based on client ones ball position
        a, b = arr[1].split('|')[0], arr[1].split('|')[1]
        ball.online_update(a, b)

        # get scores
        try:
            player.score, enemy.score = arr[2].split(',')
        except IndexError as e:
            print(e)

        # player.score, enemy.score = arr[2].split(',')[0], arr[2].split(',')[1]
        # scores = [player.score, enemy.score]
        # scores[0], scores[1] = s1, s2
        is_player_two = True

    elif '.' in data:
        arr = data.split('.')
        x, y = arr[1], arr[2]
        # print(x, y)
        # enemy = Paddle(x, y)
        enemy.online_update(x, y)
        # update ball normally
        ball.update()
        is_player_two = False
    elif 'player' or 'enemy' in data:
        if 'player' in data:
            winner = 'player'
        elif 'enemy' in data:
            winner = 'enemy'


def game_loop():
    global finished, state, n, display, is_player_two, player, player_one

    while not finished:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    finished = True

        if state == 'offline':
            display.fill(dark_gray)
            draw_dashed_line()
            draw_scores()
            check_winner()
            
            player.update()
            ai.ai_update(ball.y)
            ball.update()

            #   updating objects and screen
            pygame.display.update()
        elif state == 'online_wait':
            display.fill(dark_gray)
            waiting_text = largeFont.render('Waiting...', True, white, dark_gray)
            display.blit(waiting_text, (450, 260))
            pygame.display.update()

            data = n.rcv(4096)
            if ':' in data:
                arr = data.split(':')
                print(arr)
                n.id = arr[0]
                state = 'online_game'
                print('started game...')

        elif state == 'online_game':
            # sending client data based on user
            if is_player_two:
                response = f'{n.id}.{player.x}.{player.y}'
                n.snd(response)
            elif not is_player_two:
                try:
                    response = f'{n.id}.{player.x}.{player.y}:{ball.x}|{ball.y}:{scores[0]},{scores[1]}'
                    n.snd(response)
                except IndexError:
                    response = f'{n.id}.{player.x}.{player.y}:{ball.x}|{ball.y}'
                    n.snd(response)

            # updating objects and screen
            display.fill(dark_gray)

            player.update()
            # handle incoming network data
            handle_network()

            draw_scores()
            draw_dashed_line()
            check_winner()
            pygame.display.update()


def menu():
    global ip, finished, display, n, state, is_player_two, player, enemy, username
    print("Hello and welcome to pong-multiplayer by @stoozy\nWhat would you like to do?")
    print("1. Join a game\n2. Play vs computer (you won't win) ")
    choice = int(input("Enter choice:"))

    if choice == 2:
        state = 'offline'
        display = pygame.display.set_mode(res)
        player = Paddle(20, 330)
        finished = False
        game_loop()
    else:
        state = 'online'
        join_ip = str(input("What is the IP of the host?\nIP:"))
        finished = False
        username = input('Username:')
        n = Network(username, ip=join_ip, port=59555)

        if n.state == 'wait':
            print('waiting for other player...')
            state = 'online_wait'
            is_player_two = False
            player = Paddle(20, 330)
            enemy = Paddle(1200, 330)

            display = pygame.display.set_mode(res)
            game_loop()

        elif n.state == 'start':
            state = 'online_game'
            print('started game...')

            if n.id == '0':
                is_player_two = False
                player = Paddle(20, 330)
                enemy = Paddle(1200, 330)
            else:
                is_player_two = True
                player = Paddle(1200, 330)
                enemy = Paddle(20, 330)

            display = pygame.display.set_mode(res)
            game_loop()


if __name__ == '__main__':
    menu()
