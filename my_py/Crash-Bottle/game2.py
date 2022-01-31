import random # For generating random numbers
import sys # We will use sys.exit to exit the program
import pygame
from pygame.locals import * # Basic pygame imports
# Global Variables for the game
FPS = 40
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'gallery/sprites/player1.png'
BOTTLE = 'gallery/sprites/bottle.png'
BACKGROUND = 'gallery/sprites/background.png'
PLAYGROUND = 'gallery/sprites/playground.jpg'
PIPE = 'gallery/sprites/stand.png'
GUN = 'gallery/sprites/gun.png'
CURRENT_PLAYER_SCORE = None
HIGHSCORE = []
def welcomeScreen():
    """
    Shows welcome images on the screen
    """
    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['bottle'].get_height())/2)-50
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    messagey = int(SCREENHEIGHT*0.01)
    basex = 0
    justcount = 0
    global CURRENT_PLAYER_SCORE
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
                with open('score.txt','r') as f:
                    str1 = f.read()
                    list1 = str1.split(',')
                    
                    for i in list1:
                        HIGHSCORE.append(int(i))
                   
              
            
                
                    # print(CURRENT_PLAYER_SCORE)
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))    
                SCREEN.blit(GAME_SPRITES['bottle'], (playerx+20, playery+50))    
                SCREEN.blit(GAME_SPRITES['message'], (SCREENWIDTH/7,messagey )) 
                SCREEN.blit(GAME_SPRITES['index'], (SCREENWIDTH/4+10,messagey + 130 ))
                SCREEN.blit(GAME_SPRITES['tap'], (playerx-20 , playery+180))    
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))    
                SCREEN.blit(GAME_SPRITES['gun'], (SCREENWIDTH-38, SCREENHEIGHT/2))
               
                # score = 10
                font = pygame.font.Font('freesansbold.ttf',14)
                if CURRENT_PLAYER_SCORE != None:
                    if justcount < 12:    
                        SCREEN.blit(font.render("Your Score is : ",1, (37, 40,34)), (50,GROUNDY+3))
                        SCREEN.blit(font.render(f"{CURRENT_PLAYER_SCORE}",1, (37, 40, 35)), (155,GROUNDY+3))
                    else:
                        justcount = 0 
                        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))    
                        CURRENT_PLAYER_SCORE = None    
                    justcount += 1    
                font = pygame.font.Font('freesansbold.ttf',20)
                SCREEN.blit(font.render("Highscores : ",1, (128, 0, 66)), (10,GROUNDY+32))
                font = pygame.font.Font('freesansbold.ttf',14)
                SCREEN.blit(font.render("H1 =) ",1, (0, 0, 51)), (140,GROUNDY+36))
                SCREEN.blit(font.render(f"{HIGHSCORE[0]}",1, (0, 0, 51)), (185,GROUNDY+36))
                SCREEN.blit(font.render("H2 =) ",1, (0, 0, 51)), (140,GROUNDY+60))
                SCREEN.blit(font.render(f"{HIGHSCORE[1]}",1, (0, 0, 51)), (185,GROUNDY+60))
                SCREEN.blit(font.render("H3 =) ",1, (0, 0, 51)), (140,GROUNDY+84))
                SCREEN.blit(font.render(f"{HIGHSCORE[2]}",1, (0, 0, 51)), (185,GROUNDY+84))

                
                pygame.display.update()
                FPSCLOCK.tick(FPS)
    
def mainGame():
    global CURRENT_PLAYER_SCORE
    global HIGHSCORE
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH) - 30
    basex = 0
    count = 0

    # Create 3 pipes for blitting on the screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()
    newPipe3 = getRandomPipe()
    # my List of upper pipes

    upperPipes = [
        {'x': SCREENWIDTH+150, 'y':newPipe1['y']},
        {'x': SCREENWIDTH+180+(SCREENWIDTH/2), 'y':newPipe2['y']}
    ]
    
    pipeVelX = -4

    playerVelY = -15
    playerMaxVelY = 10
    playerMinVelY = -14
    playerAccY = 1

    playerFlapAccv = -8 # velocity while flapping
    playerFlapped = False # It is true only when the bird is flapping
    
    bullet = 5
    count_bullet = 0
    while True:
        # mx,my =pygame.mouse.get_pos()
        # if my > 398:
        #     my = 398
        
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     mx,click = pygame.mouse.get_pos()
            #     upperPipes.append({'x': SCREENWIDTH-130 , 'y':click-15})         
       
        # count+=1
        # if count>39:
        #     mx,click = pygame.mouse.get_pos()
        #     upperPipes.append({'x': SCREENWIDTH-130 , 'y':my-15})         
        #     count=0
        crashTest = isCollide(playerx-42, playery-13, upperPipes) # This function will return true if the player is crashed
        if crashTest:
            CURRENT_PLAYER_SCORE = score
            with open('score.txt','r') as f:
                str1 = f.read()
                list1 = str1.split(',')
                list2=[]
                for i in list1:
                    list2.append(int(i))
                list2.append(score)    
                list2.sort()
                list2.reverse() 
                list2.pop(3)   
                
            f = open("score.txt", "w")
            f.writelines([f'{list2[0]},',f'{list2[1]},',f'{list2[2]}'])
            f.close()
            return     
        if score%90==0 and score!=0:
            GAME_SOUNDS['success'].play()

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
        if len(upperPipes)!=0: 
            for upperPipe  in upperPipes:
                upperPipe['x'] += pipeVelX
            
        # # Lets blit our sprites now
        SCREEN.blit(GAME_SPRITES['playground'], (0, 0))
        # SCREEN.blit(GAME_SPRITES['gun'], (SCREENWIDTH-38, my))  
       
        if score >290:
            bullet = 25
        if score > 200:
            bullet = 23
        if score> 140:
            bullet = 21   
        if score >85:
            bullet =19

        if score>55:
            bullet = 17
        
        if score >35:
            bullet = 14          
        
        if score>10:
            bullet = 8
        
        if len(upperPipes)!=0:
            if 0 < upperPipes[0]['x'] <bullet:
                MyList = [370,200,40]
                ry = random.choice(MyList)
                if score%2==0:
                    upperPipes.append({'x':SCREENWIDTH+10,'y':ry})
                    upperPipes.append({'x':SCREENWIDTH+10,'y':ry})
                newpipe = getRandomPipe()
                upperPipes.append(newpipe)
            if upperPipes[0]['x'] < -GAME_SPRITES['pipe'].get_width():
                upperPipes.pop(0)
            for upperPipe in upperPipes:
                SCREEN.blit(GAME_SPRITES['pipe'], (upperPipe['x'], upperPipe['y']))
        if len(upperPipes)==0:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe)

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
        font = pygame.font.Font('freesansbold.ttf',20)
        SCREEN.blit(font.render("Your Score : ",1, (128, 0, 66)), (50,GROUNDY+(SCREENHEIGHT-GROUNDY)/2))
        SCREEN.blit(font.render(f"{score}",1, (0, 0, 51)), (170,GROUNDY+(SCREENHEIGHT-GROUNDY)/2))    
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def isCollide(playerx, playery, upperPipes):
    # if playery> GROUNDY - 70  or playery<0:
    #     GAME_SOUNDS['hit'].play()
    #     return True
    playerHeight = GAME_SPRITES['player'].get_height()
    playerWidth = GAME_SPRITES['player'].get_width()
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'].get_height()
        pipeWidth = GAME_SPRITES['pipe'].get_width()
        if( ( (playery>pipe['y'] and playery+30 < (pipeHeight + pipe['y'])) or ( (playery+playerHeight) < (pipeHeight + pipe['y']) and (playery + playerHeight)>pipe['y'] ))\
            and ((playerx>pipe['x'] and playerx+82< (int(pipeWidth + pipe['x']))) or ( (playerx + playerWidth)>pipe['x'] and (playerx+playerWidth+82) < (pipeWidth + pipe['x']) ) ) ):
            GAME_SOUNDS['success'].stop()
            GAME_SOUNDS['hit'].play()         
            # print('playerx :',playerx+82)
            # print('pipex :',pipe['x'])
            # print('pipewidth :',pipeWidth)
            # print('pipewidth + pipex :',pipeWidth+pipe['x'])
                # abs(playerx - pipe['x']) < GAME_SPRITES['pipe'].get_width()):
                    # GAME_SOUNDS['hit'].play()
            return True
        if playery>347 and pipe['y']>347:
            if playerx+40==pipe['x']:
                return True     
    
    # for pipe in upperPipes:
    #     pipeHeight = GAME_SPRITES['pipe'].get_height()
    #     if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
    #         GAME_SOUNDS['hit'].play()
    #         return True

    return False


def getRandomPipe():
    """
    Generate positions of pipes for blitting on the screen
    """
    pipeHeight = GAME_SPRITES['pipe'].get_height()
    offset = random.randrange(1,50)
    y1 = offset+random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() ))
    pipeX = SCREENWIDTH + random.randrange(5,25)
    if y1>383:
        y1 =382 
    pipe = {'x': pipeX, 'y': y1}
    return pipe

if __name__ == "__main__":
    # This will be the main point from where our game will start
    pygame.init() # Initialize all pygame's modules
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Bottle Crash Game')
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
    GAME_SPRITES['message'] =pygame.image.load('gallery/sprites/first.png').convert_alpha()
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
    GAME_SOUNDS['success'] = pygame.mixer.Sound('gallery/audio/success.wav')

    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['playground'] = pygame.image.load(PLAYGROUND).convert()

    GAME_SPRITES['bottle'] = pygame.image.load(BOTTLE).convert_alpha()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()
    GAME_SPRITES['gun'] = pygame.image.load(GUN).convert_alpha()
    while True:
        welcomeScreen() # Shows welcome screen to the user until he presses a button
        mainGame() # This is the main game function 