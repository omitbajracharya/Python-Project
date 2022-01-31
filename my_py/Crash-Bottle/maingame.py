import random,sys,pygame,math
from pygame.locals import * 
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
OBS = 'gallery/sprites/obs.png'
CURRENT_PLAYER_SCORE = 0
HIGHSCORE = [0,0,0]
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
    global HIGHSCORE
     # if event.type == pygame.MOUSEBUTTONDOWN:
            #     mx,click = pygame.mouse.get_pos()
            #     obstacles.append({'x': SCREENWIDTH-130 , 'y':click-15})         
    while True: 
        for event in pygame.event.get():
            # if user clicks on cross button, close the game
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            # If the user presses space or up key, start the game for them
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key == K_UP):
                mainGame()
            else:
                with open('score.txt','r') as f:
                    str1 = f.read()
                    l = str1.split(',')
                    HIGHSCORE[0],HIGHSCORE[1],HIGHSCORE[2] = l
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))    
                SCREEN.blit(GAME_SPRITES['bottle'], (playerx+20, playery+50))    
                SCREEN.blit(GAME_SPRITES['message'], (SCREENWIDTH/7,messagey )) 
                SCREEN.blit(GAME_SPRITES['index'], (SCREENWIDTH/4+10,messagey + 130 ))
                SCREEN.blit(GAME_SPRITES['tap'], (playerx-20 , playery+180))    
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
                font = pygame.font.Font('freesansbold.ttf',20)
                SCREEN.blit(font.render("Highscore : ",1, (128, 0, 66)), (50,GROUNDY+(SCREENHEIGHT-GROUNDY)/2))
                SCREEN.blit(font.render(f"{HIGHSCORE[0]}",1, (0, 0, 51)), (170,GROUNDY+(SCREENHEIGHT-GROUNDY)/2))
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

    # Create 2 obstacles initially for blitting on the screen
    newObs1 = get_Obstacle()
    newObs2 = get_Obstacle()
    obstacles = [
        {'x': SCREENWIDTH+150, 'y':newObs1['y']},
        {'x': SCREENWIDTH+180+(SCREENWIDTH/2), 'y':newObs2['y']}
    ]
    
    obsVelX = -4

    playerVelY = -15
    playerMaxVelY = 10
    playerMinVelY = -14
    playerAccY = 1

    playerFlapAccv = -8 # velocity while flapping
    playerFlapped = False # It is true only when the bird is flapping
    
    distance = 5
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
        crashTest = isCollide(playerx-42, playery-13, obstacles) # This function will return true if the player is crashed
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
                HIGHSCORE = list2
            f = open("score.txt", "w")
            f.writelines([f'{list2[0]},',f'{list2[1]},',f'{list2[2]}'])
            f.close()
            displaysection()
        if score%90==0 and score!=0:
            GAME_SOUNDS['success'].play()

        #check for score
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for obst in obstacles:
            oMidPos = obst['x'] + GAME_SPRITES['obs'].get_width()/2
            if oMidPos<= playerMidPos < oMidPos +4:
                score +=1
                print(f"Your score is {score}") 
                GAME_SOUNDS['point'].play()


        if playerVelY <playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False            
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)
        
        # move obstacles to the left
        if len(obstacles)!=0: 
            for obstacle  in obstacles:
                obstacle['x'] += obsVelX
            
        if score >290:
            distance = 25
        if score > 200:
            distance = 23
        if score> 140:
            distance = 21   
        if score >85:
            distance =19
        if score>55:
            distance = 17
        if score >35:
            distance = 14          
        if score>10:
            distance = 8
        SCREEN.blit(GAME_SPRITES['playground'], (0, 0)) 
        if len(obstacles)!=0:
            if 0 < obstacles[0]['x'] <distance:
                MyList = [370,200,40]
                ry = random.choice(MyList)
                if score%2==0:
                    obstacles.append({'x':SCREENWIDTH+10,'y':ry})
                    obstacles.append({'x':SCREENWIDTH+10,'y':ry})
                newobs = get_Obstacle()
                obstacles.append(newobs)
            if obstacles[0]['x'] < -GAME_SPRITES['obs'].get_width():
                obstacles.pop(0)
            for obstacle in obstacles:
                SCREEN.blit(GAME_SPRITES['obs'], (obstacle['x'], obstacle['y']))
        if len(obstacles)==0:
            newobs = get_Obstacle()
            obstacles.append(newobs)

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

def isCollide(playerx, playery, obstacles):
    # if playery> GROUNDY - 70  or playery<0:
    #     GAME_SOUNDS['hit'].play()
    #     return True
    playerHeight = GAME_SPRITES['player'].get_height()
    playerWidth = GAME_SPRITES['player'].get_width()
    for obst in obstacles:
        oHeight = GAME_SPRITES['obs'].get_height()
        oWidth = GAME_SPRITES['obs'].get_width()
        if( ( (playery>obst['y'] and playery+30 < (oHeight + obst['y'])) or ( (playery+playerHeight) < (oHeight + obst['y']) and (playery + playerHeight)>obst['y'] ))\
            and ((playerx>obst['x'] and playerx+82< (int(oWidth + obst['x']))) or ( (playerx + playerWidth)>obst['x'] and (playerx+playerWidth+82) < (oWidth + obst['x']) ) ) ):
            GAME_SOUNDS['success'].stop()
            GAME_SOUNDS['hit'].play()         
            return True
        if playery>347 and obst['y']>347:
            if playerx+40==obst['x']:
                return True     
    return False


def get_Obstacle():
    """
    Generate positions of os for blitting on the screen
    """
    y1 = random.randrange(3, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() ))
    obsX = SCREENWIDTH + random.randrange(5,25)
    if y1>383:
        y1 =382 
    obst = {'x': obsX , 'y': y1}
    return obst

def displaysection():
    
    global CURRENT_PLAYER_SCORE
    global HIGHSCORE  
    playbtn = pygame.image.load('gallery/sprites/play.png').convert_alpha()
    highscore = pygame.image.load('gallery/sprites/highscore.png').convert_alpha()
    gameover = pygame.image.load('gallery/sprites/gameover.png').convert_alpha()
    mainscrn = pygame.image.load('gallery/sprites/mainscrn.png').convert_alpha()
    playx = 40
    playy = 413 
    mainx = playx+140
    mainy = playy
    while True: 
        for event in pygame.event.get():
            # if user clicks on cross button, close the game
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            # If the user presses space or up key, start the game for them
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key == K_UP):
                mainGame()
            elif event.type == pygame.MOUSEBUTTONDOWN:    
                     
                mx,my = pygame.mouse.get_pos()
                playcenter = playbtn.get_width()/2
                x = playx + playcenter
                y = playy + playcenter
                r  = playcenter 
                sqx = (mx - x)**2
                sqy = (my - y)**2
                #x^2 + y^2 < r^2    --->inside circle   
                #=>( sqrt of x^2 + y^2 ) < r 
                if math.sqrt(sqx + sqy) < r:
                    mainGame()


                maincenter = mainscrn.get_width()/2 
                m = mainx + maincenter
                n = mainy + maincenter
                sqx = (mx - m)**2
                sqy = (my - n)**2
                if math.sqrt(sqx + sqy) < maincenter:
                    welcomeScreen()

            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))
                SCREEN.blit(gameover, (20, 20))
                font = pygame.font.Font('freesansbold.ttf',25)
                SCREEN.blit(highscore, (20, 180))   
                font = pygame.font.Font('freesansbold.ttf',20)            
                SCREEN.blit(font.render(f"{HIGHSCORE[0]}",1, (0, 0, 51)), (128,272))
                SCREEN.blit(font.render(f"{HIGHSCORE[1]}",1, (0, 0, 51)), (128,312))
                SCREEN.blit(font.render(f"{HIGHSCORE[2]}",1, (0, 0, 51)), (128,350))    
                SCREEN.blit(font.render("Your Score is : ",1, (0, 0, 51)), (30,390))
                SCREEN.blit(font.render(f"{CURRENT_PLAYER_SCORE}",1, (37, 40, 35)), (178,390))
                SCREEN.blit(playbtn, (playx, playy))
                SCREEN.blit(font.render("Play Again",1, (255, 51, 51)), (playx-18,playy+57))
                SCREEN.blit(mainscrn, (mainx, mainy))
                SCREEN.blit(font.render("Mainscreen",1, (255, 51, 51)), (mainx-20,playy+57))
                pygame.display.update()
                
    

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
    GAME_SPRITES['index'] =pygame.image.load('gallery/sprites/index.png').convert_alpha()
    GAME_SPRITES['tap'] =pygame.image.load('gallery/sprites/tap.png').convert_alpha()
    GAME_SPRITES['base'] =pygame.image.load('gallery/sprites/base.png').convert_alpha()
    GAME_SPRITES['obs'] =(pygame.transform.rotate(pygame.image.load(OBS).convert_alpha(), 90))

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
    welcomeScreen() # Shows welcome screen to the user until he presses a button