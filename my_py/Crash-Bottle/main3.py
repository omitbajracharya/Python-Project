import random # For generating random numbers
import sys # We will use sys.exit to exit the program
import pygame
from pygame.locals import * # Basic pygame imports

# Global Variables for the game
FPS = 35
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'gallery/sprites/player1.png'
BOTTLE = 'gallery/sprites/bottle.png'
BACKGROUND = 'gallery/sprites/background.png'
PIPE = 'gallery/sprites/stand.png'

def welcomeScreen():
    """
    Shows welcome images on the screen
    """
    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['bottle'].get_height())/2)-50
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    messagey = int(SCREENHEIGHT*0.01)
    basex = 0
    while True:
        
        for event in pygame.event.get():
            # if user clicks on cross button, close the game
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # If the user presses space or up key, start the game for them
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))    
                SCREEN.blit(GAME_SPRITES['bottle'], (playerx, playery+50))    
                SCREEN.blit(GAME_SPRITES['message'], (messagex,messagey )) 
                SCREEN.blit(GAME_SPRITES['index'], (messagex,messagey + 130 ))
                SCREEN.blit(GAME_SPRITES['tap'], (playerx-20 , playery+180))    
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))    
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def mainGame():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)
    basex = 0

    # Create 2 pipes for blitting on the screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()
    newPipe3 = getRandomPipe()
    # my List of upper pipes

    upperPipes = [
        {'x': SCREENWIDTH+150, 'y':newPipe1['y']},
        {'x': SCREENWIDTH+180+(SCREENWIDTH/2), 'y':newPipe2['y']},
        {'x': SCREENWIDTH+280+(SCREENWIDTH/2), 'y':newPipe3['y']}
    ]
    
    pipeVelX = -4

    playerVelY = -12
    playerMaxVelY = 10
    playerMinVelY = -10
    playerAccY = 1

    playerFlapAccv = -8 # velocity while flapping
    playerFlapped = False # It is true only when the bird is flapping


    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()

    
        crashTest = isCollide(playerx, playery, upperPipes) # This function will return true if the player is crashed
        if crashTest:
            return     

        #check for score
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'].get_width()/2
            if pipeMidPos<= playerMidPos < pipeMidPos +4:
                score +=1
                print(f"Your score is {score}") 
                GAME_SOUNDS['point'].play()


        if playerVelY <playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False            
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

        # move pipes to the left
        for upperPipe  in upperPipes:
            upperPipe['x'] += pipeVelX
            # lowerPipe['x'] += pipeVelX
            # print(upperPipe)
        # print(upperPipe)    
        # Add a new pipe when the first is about to cross the leftmost part of the screen
        if 0 < upperPipes[0]['x'] <6:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe)
            
        # if the pipe is out of the screen, remove it
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'].get_width():
            upperPipes.pop(0)
        #     # lowerPipes.pop(0)
        
        # # Lets blit our sprites now
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe in upperPipes:
            SCREEN.blit(GAME_SPRITES['pipe'], (upperPipe['x'], upperPipe['y']))

        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def isCollide(playerx, playery, upperPipes):
    if playery> GROUNDY - 60  or playery<0:
        GAME_SOUNDS['hit'].play()
        return True
    playerHeight = GAME_SPRITES['player'].get_height();
    playerWidth = GAME_SPRITES['player'].get_width();
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'].get_height()
        pipeWidth = GAME_SPRITES['pipe'].get_width()
        if( ( (playery>pipe['y'] and playery < (pipeHeight + pipe['y'])) or ( (playery+playerHeight) < (pipeHeight + pipe['y']) and (playery + playerHeight)>pipe['y'] ))\
            and ((playerx>pipe['x'] and playerx < (pipeWidth + pipe['x'])) or ( (playerx + playerWidth)>pipe['x'] and (playerx+playerWidth) < (pipeWidth + pipe['x']) ) ) ):
            GAME_SOUNDS['hit'].play()         
                # abs(playerx - pipe['x']) < GAME_SPRITES['pipe'].get_width()):
                    # GAME_SOUNDS['hit'].play()
            return True
    
    return False


def getRandomPipe():
    """
    Generate positions of pipes for blitting on the screen
    """
    pipeHeight = GAME_SPRITES['pipe'].get_height()
    offset = SCREENHEIGHT/3
    y1 = random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height()  - 0.08 *offset))
    pipeX = SCREENWIDTH + random.randrange(5,15)
    pipe = {'x': pipeX, 'y': y1}
    
    return pipe

if __name__ == "__main__":
    # This will be the main point from where our game will start
    pygame.init() # Initialize all pygame's modules
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flip Bottle Game')
    GAME_SPRITES['numbers'] = ( 
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha(),
    )
    GAME_SPRITES['message'] =pygame.image.load('gallery/sprites/index.png').convert_alpha()
    GAME_SPRITES['index'] =pygame.image.load('gallery/sprites/index4.png').convert_alpha()
    GAME_SPRITES['tap'] =pygame.image.load('gallery/sprites/tap.png').convert_alpha()
    GAME_SPRITES['base'] =pygame.image.load('gallery/sprites/base.png').convert_alpha()
    GAME_SPRITES['pipe'] =(pygame.transform.rotate(pygame.image.load( PIPE).convert_alpha(), 90))

    # Game sounds
    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['bottle'] = pygame.image.load(BOTTLE).convert_alpha()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()
    while True:
        welcomeScreen() # Shows welcome screen to the user until he presses a button
        mainGame() # This is the main game function 