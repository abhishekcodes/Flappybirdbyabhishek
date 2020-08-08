import random #for generating random numbers
import sys #used to exit the program
import pygame 
from pygame.locals import *  #basic pygame imports

#Global variables for game
FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'Gallery/sprites/bird.png'
BACKGROUND ='Gallery/sprites/bg.png'
PIPE = 'Gallery/sprites/pipe.png'

def welcomeScreen():
    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
    x = int((SCREENWIDTH - GAME_SPRITES['message'].get_height())/2)
    y = int(SCREENHEIGHT*0.13)
    basex = 0 
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                return 
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0,0))
                SCREEN.blit(GAME_SPRITES['player'], (playerx,playery))
                SCREEN.blit(GAME_SPRITES['message'], (10,20))
                SCREEN.blit(GAME_SPRITES['base'], (basex,GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def mainGame():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENHEIGHT/2)
    basex = 0

    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    #list of upper pipes
    upperPipes = [
        {'x': SCREENWIDTH+200, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y': newPipe2[0]['y']},
    ]
    #list of lower pipes
    lowerPipes = [
        {'x': SCREENWIDTH+200, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y': newPipe2[1]['y']},
    ]
    
    pipeVelX = -4

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8
    playerFlapped = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playery = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()
        
        crashTest = isCollide(playerx,playery,upperPipes,lowerPipes)

        if crashTest:
            return

        playermidPos = playerx + GAME_SPRITES.get_width()/2
        for pipe in upperPipes:
            pipemidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipemidPos <= playermidPos < pipemidpos + 4:
                score +=1
                print(f"your score is {score}")
                GAME_SOUNDS['point'].play()

        if playerVelY < playerMaxVelY and not playerFlapped :
            player += playerAccY
        
        if playerFlapped:
            playerFlapped = False

        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY,GROUNDY- playery - playerHeight)

        #move pipes to the left
        for upperPipes,lowerPipes in zip(upperPipes,lowerPipes):
            upperPipes['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        #add a new pipe when first one clears the screen
        if 0<upperPipes[0]['x']<5 :
            newPipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])


        #if pipe is out of the screen, remove it
        if upperPipes[0]['x'] < - GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        SCREEN.blit(GAME_SPRITES['background'],(0,0))

        for upperPipe, lowerPipe in zip(upperPipes,lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0],(upperPipe['x'],upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1],(lowerPipe['x'],lowerPipe['y']))

        SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))

        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit],(xoffset,SCREENHEIGHT*0.12))
            xoffset += GAME_SPRITES['numbers'][digit].get_width()
            pygame.display.update()
            FPSCLOCK.tick(FPS)

def isCollide(playerx,playery,upperPipes,lowerPipes):
    if playery > GROUNDY - 25 or player<0:
        GAME_SOUNDS['hit'].play()
        return True

    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery<pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True
    return False

def getRandomPipe():
    #generate position of two pipes
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0,int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2*offset))
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x' : pipeX, 'y' : -y1},
        {'x' : pipeX, 'y' : y2},
    ]

    return pipe



if __name__ == "__main__":
    #This will be the main fn from where the game will start
    pygame.init() #initialize all pygame  modules
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird by ABhishek')
    GAME_SPRITES['numbers'] = (
        pygame.image.load('Gallery/sprites/zero.png').convert_alpha(),
         #convert_alpha changes image pixel and alpha
        pygame.image.load('Gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('Gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('Gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('Gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('Gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('Gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('Gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('Gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('Gallery/sprites/8.png').convert_alpha(),
    )

    GAME_SPRITES['message'] = pygame.image.load('Gallery/sprites/msg.png').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('Gallery/sprites/base.png').convert_alpha()
    GAME_SPRITES['pipe'] = (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180),
        pygame.image.load(PIPE).convert_alpha()
    )

    #Game sounds
    GAME_SOUNDS['die'] = pygame.mixer.sound('Gallery/audio/die.mp3')
    GAME_SOUNDS['hit'] = pygame.mixer.sound('Gallery/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.sound('Gallery/audio/point.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.sound('Gallery/audio/wing.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.sound('Gallery/audio/swoosh.wav')

    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    while True:
        welcomeScreen() #shows welcome screen until button is pressed
        mainGame() 