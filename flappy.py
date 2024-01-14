# Mario
# Date: 01 / jan / 1999
# Author: Edgar A. M.

import pygame
import sys
import random

""" Preload images """
pipe_day = pygame.image.load("pipe_green.png")
pipe_night = pygame.image.load("pipe_red.png")

""" Bird object """
class Bird(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()

        # sounds
        self.flap = pygame.mixer.Sound('wing.wav')
        self.crash = pygame.mixer.Sound('crash.wav')
        
        # flapping sprites
        self.sprites = []

        for i in [1, 2, 3]:
            temp = pygame.image.load(color + str(i) + ".png").convert_alpha()
            temp = pygame.transform.scale2x(temp)
            self.sprites.append(temp)
            
        # current sprite
        self.image = self.sprites[0]

        # temporary sprite
        self.temporary = self.image

        # current rectangle
        self.rect = self.image.get_rect(center=(BIRD_X, HEIGHT/2))

        # current frame
        self.frame = 0

        # movement amount
        self.movement = 0
      
    def fall(self):
        # bird falls with accelerated motion
        self.movement += GRAVITY
        self.rect.centery += self.movement

    def rotate(self):
        # factor is positive when falling, therefore rotation is clockwise
        # factor is negative when raising, rotation is counter-clockwise
        factor = -2
        factor *= self.movement

        self.image = pygame.transform.rotozoom(self.temporary, factor, 1)
        
    def animate(self):
        # loop through sprites
        if self.frame < 2:
            self.frame += 1
        else:
            self.frame = 0

        self.image = self.sprites[self.frame]
        self.temporary = self.image

    def check(self, _pipes):
        # declare GAMEOVER as a global variable in order to change it
        global GAMEOVER

        # pipe collision
        for _pipe in _pipes:
            if self.rect.colliderect(_pipe):
                GAMEOVER = True
                self.crash.play()
                
        # boundaries collision
        if self.rect.top <= CEILING or self.rect.bottom >= FLOOR:
            GAMEOVER = True
            self.crash.play()
  
    def update(self, _pipes):
        if not GAMEOVER:
            self.fall()
            self.rotate()
            self.check(_pipes)
        # move it out of the screen if game is over!
        else:
            self.rect = self.image.get_rect(center=(-BIRD_X, HEIGHT/2))

""" Background object """
class Background():
    def __init__(self, daytime):
        if daytime == 'day':
            file = 'background_day.png'
        if daytime == 'night':
            file = 'background_night.png'

        self.image = pygame.image.load(file).convert()
        self.image = pygame.transform.scale2x(self.image)

    def update(self):
        screen.blit(self.image, (0, 0))

""" Floor object """
class Floor():
    def __init__(self):
        self.image = pygame.image.load('floor.png').convert()
        self.image = pygame.transform.scale2x(self.image)
        self.x = 0

    def move(self):
        self.x -= 1

        if self.x <= -WIDTH:
            self.x = 0

    def update(self):
        self.move()
        screen.blit(self.image, (self.x, FLOOR))
        screen.blit(self.image, (self.x + WIDTH, FLOOR))

""" Pipes """
class Lower(pygame.sprite.Sprite):
    def __init__(self, daytime, offset):
        super().__init__()

        if daytime == 'day':
            self.image = pipe_day
        if daytime == 'night':
            self.image = pipe_night

        self.image = pygame.transform.scale2x(self.image)
        self.rect = self.image.get_rect(midtop=(WIDTH, HEIGHT/2))

        self.amount = 5

        # set pipes apart
        self.rect.centery += GAP / 2

        # displace pipes by a random amount
        self.rect.centery += offset

    def update(self):
        global SCORE
        
        self.rect.x -= self.amount
        if self.rect.right <= 0:
            self.kill()
            # score increases once the pipes disappear
            SCORE += 1
        elif GAMEOVER:
            self.kill()

class Upper(pygame.sprite.Sprite):
    def __init__(self, daytime, offset):
        super().__init__()

        if daytime == 'day':
            self.image = pipe_day
        if daytime == 'night':
            self.image = pipe_night

        self.image = pygame.transform.scale2x(self.image)
        self.image = pygame.transform.flip(self.image, 0, 1)
        self.rect = self.image.get_rect(midbottom=(WIDTH, HEIGHT/2))

        self.amount = 5

        # set pipes apart
        self.rect.centery -= GAP / 2

        # displace pipes by a random amount
        self.rect.centery += offset

    def update(self):
        self.rect.x -= self.amount
        if self.rect.right <= 0 or GAMEOVER:
            self.kill()

""" Message """
class Message():
    def __init__(self):
        self.image = pygame.image.load('message.png').convert_alpha()
        self.image = pygame.transform.scale2x(self.image)
        self.rect = self.image.get_rect(center=(WIDTH/2, HEIGHT/2))

    def update(self):
        if GAMEOVER == True:
            screen.blit(self.image, self.rect)

""" Display """
class Display():
    def __init__(self):
        self.high = [0]
        self.font = pygame.font.Font('04B_19.TTF', 32)
        self.switch = False

    def update(self):
        global SCORE

        # text color
        color = (255, 255, 255)

        # this statement is only executed once right after game over,
        # the switch makes sure that this happens only once, that is,
        # the last score is appended to the highest scores list.
        if GAMEOVER == True and self.switch == False:
            self.high.append(SCORE)
            SCORE = 0
            self.switch = True
            
        # highest score
        text = 'HI ' + str(max(self.high)).zfill(3)
        pos = (WIDTH/2 - 128, 64)     
        screen.blit(self.font.render(text, True, color), pos)

        # current score
        text = str(SCORE).zfill(3)
        pos = (WIDTH/2 + 32, 64)   
        screen.blit(self.font.render(text, True, color), pos)
              
""" Game variables """
WIDTH = 576                     # screen width
HEIGHT = 1024                   # screen height
FLOOR = 900		        # bottom of the floor (measured from top to bottom)
CEILING = -100 			# ceiling position (above the top of the screen)
BIRD_X = 100			# bird's position from the left wall
GRAVITY = 0.25 			# gravity (pixels increment)
JUMP = 7.5			# bird's jump (amount in pixels)
GAP = 250			# distance between pipes (less is harder to play)
PIPE_FREQ = 1200		# pipe show-up frequency in mS
FLAP_FREQ = 200			# flap frequency in mS
DAYTIME = 'day'                 # play game daytime
COLOR = 'blue'                  # bird color
SCORE = 0                       # number of pairs cleared
GAMEOVER = False 		# game status condition

""" Settings """
pygame.mixer.pre_init(44100, -16, 2, 512)       # sounds settings
pygame.init()                                   # init module
pygame.mouse.set_visible(False)                 # no mouse cursor
clock = pygame.time.Clock()                     # create clock	
SPAWNPIPE = pygame.USEREVENT                    # pipe creation event  
BIRDFLAP = pygame.USEREVENT + 1	                # bird flap event
pygame.time.set_timer(SPAWNPIPE, PIPE_FREQ)     # pipe timer
pygame.time.set_timer(BIRDFLAP, FLAP_FREQ)      # flap timer

""" Objects """
screen = pygame.display.set_mode((WIDTH, HEIGHT))
background = Background(DAYTIME)
floor = Floor()
message = Message()
upper_pipes= pygame.sprite.Group()
lower_pipes= pygame.sprite.Group()
pipes = []
display = Display()
bird = pygame.sprite.GroupSingle(Bird(COLOR))

""" Main Loop """
while True:

    # Event handler
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            if event.key == pygame.K_SPACE:
                bird.sprite.movement = 0        # keep bird still
                bird.sprite.movement -= JUMP    # move it upwards
                bird.sprite.flap.play()         # flap sound

            if event.key == pygame.K_SPACE and GAMEOVER:
                # random scenario each new game
                DAYTIME = random.choice(['day', 'night'])
                COLOR = random.choice(['blue', 'red', 'yellow'])
                background = Background(DAYTIME)
                bird = pygame.sprite.GroupSingle(Bird(COLOR))

                # reset state
                GAMEOVER = False
                display.switch = False
                pipes.clear()                               # empty pipes list
                bird.sprite.movement = 0                    # keep bird still
                bird.sprite.rect.center = (BIRD_X, HEIGHT/2)# center bird
            
        if event.type == SPAWNPIPE:
            offset = random.choice([50, 100, 150, -50, -100, -150])
            if not GAMEOVER:
                upper_pipes.add(Upper(DAYTIME, offset))
                lower_pipes.add(Lower(DAYTIME, offset))
                pipes.extend(upper_pipes)
                pipes.extend(lower_pipes)
            
        if event.type == BIRDFLAP:
            bird.sprite.animate()
                           
    # Drawing
    background.update()
    upper_pipes.draw(screen)
    lower_pipes.draw(screen)
    upper_pipes.update()
    lower_pipes.update()
    display.update()
    floor.update()
    message.update()
    bird.draw(screen)
    bird.update(pipes)
    pygame.display.flip()
    clock.tick(120)
    
