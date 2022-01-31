import random
import sys 
import pygame
from pygame.locals import * 
# Global Variables for the game
SCREENWIDTH = 600
SCREENHEIGHT = 600
pygame.init() # Initialize all pygame's modules
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption('Tic-Tac-Toe')

winner = None
a = 35
BOXPOINT=[
    (45,50+a),(230,50+a),(415,50+a),
    (45,235+a),(230,235+a),(415,235+a),
    (45,420+a),(230,420+a),(415,420+a)
]

capture = [] 
capture_dict = {}
background = pygame.image.load("gallery/bac.jpg").convert()
home = pygame.image.load("gallery/index.jpg").convert()                
box = pygame.image.load("gallery/box.jpg").convert_alpha() 
x = pygame.image.load("gallery/x.png").convert_alpha()
o = pygame.image.load("gallery/o.png").convert_alpha()                 
currentplayer = x
logicplayer ='x'
board=[
    "-","-","-","-","-","-","-","-","-"
]
versus =  pygame.image.load("gallery/versus.png").convert_alpha()           
white=(255,255,255)
black=(0,0,0)
red=(255,0,0)
flag = True
capture_position =  None
def index():
    global flag
    global board
    global winner
    global capture_position
    global capture 
    global capture_dict
    capture_position = None
    winner = None
    board=["-","-","-","-","-","-","-","-","-"]
    capture=[]
    capture_dict={}
    flag = True
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key == K_UP):
                return
            else:
                playbutton = pygame.image.load("gallery/playbutton.png").convert_alpha() 
                SCREEN.blit(home, (0,0))                
                font = pygame.font.Font('freesansbold.ttf',20)
                SCREEN.blit(font.render("-------------------------- ",1, (128, 0, 66)), (25,50))
                SCREEN.blit(font.render("__________",1, (128, 0, 66)), (220,50))
                text = font.render("Tic-Toc-Toe",True, (128, 0, 66))
                SCREEN.blit(text, (220,50))
                SCREEN.blit(font.render("Game",1, (128, 0, 66)), (250,72))
                SCREEN.blit(font.render("------------------------------ ",1, (128, 0, 66)), (350,50))
                SCREEN.blit(font.render("Code by Omit",1, (0, 0, 66)), (SCREENWIDTH-210,SCREENHEIGHT-30))                              
                SCREEN.blit(x, (100,60))
                SCREEN.blit(o, (SCREENWIDTH/2+70,66))
                SCREEN.blit(versus, (230,85))                
                bx = SCREENWIDTH/2-60
                by = SCREENHEIGHT-95
                SCREEN.blit(playbutton,(bx,by))
                # pygame.draw.rect(SCREEN,red,[50,50,50,50])
                pygame.display.update()    

                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx,my = pygame.mouse.get_pos()
                if (mx >= bx and mx <=bx +80) and (my>=by and my<=by+56) :
                    return 


def flip_player():
    global logicplayer
    global currentplayer
    if currentplayer == x:
        currentplayer = o
        logicplayer ='o'
    elif currentplayer == o:
        currentplayer =x
        logicplayer ='x'  

def occupy_box(mx,my):
    global logicplayer
    global capture_position
    global currentplayer
    if my>=50+a and my<=190+a:
        if mx>=45 and mx<=185:
            capture_position = 0 
        elif mx>=230 and mx<=370:
            capture_position = 1
        elif mx>=420 and mx<=560:
            capture_position = 2
    elif my>=235+a and my<=375+a:
        if mx>=45 and mx<=185:
            capture_position = 3
        elif mx>=230 and mx<=370:
            capture_position = 4
        elif mx>=420 and mx<=560:
            capture_position = 5
    elif my>=420+a and my<=560+a:
        if mx>=45 and mx<=185:
            capture_position = 6
        elif mx>=230 and mx<=370:
            capture_position = 7
        elif mx>=420 and mx<=560:
            capture_position = 8
    else:
        capture_position =None  

    if capture_position not in capture and capture_position != None:
        capture.append(capture_position)
        capture_dict[capture_position] = currentplayer
        board[capture_position] = logicplayer
        flip_player()


def check_Win():
    global winner
    global flag
    #check Row win
    row1 = board[0]==board[1]==board[2]!="-"
    row2 = board[3]==board[4]==board[5]!="-"
    row3 = board[6]==board[7]==board[8]!="-"
    if row1 or row2 or row3:
        flag = False
        if row1:
            winner = board[0]
        elif row2:
            winner = board[3]
        elif row3:
            winner = board[6]
        return    
    #check column win
    col1 = board[0]==board[3]==board[6]!="-"
    col2 = board[1]==board[4]==board[7]!="-"
    col3 = board[2]==board[5]==board[8]!="-"      
    if col1 or col2 or col3:
        flag = False
        if col1:
            winner = board[0]
        elif col2:
            winner = board[1]
        elif col3:
            winner = board[2]
        return   

    #check diagonal win
    diag1 = board[0]==board[4]==board[8]!="-"
    diag2 = board[2]==board[4]==board[6]!="-"
    if diag1 or diag2:
        flag = False
        if diag1:
            winner = board[0]
        elif diag2:
            winner = board[2]            
        
    return    
def check_Tie():
    global winner
    global flag
    if "-" not in board:
        flag = False
    return




def check_gameover():
    win = check_Win()
    if win:
        return
    tie = check_Tie()
    if tie:
        return

def displayboard():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT :
                pygame.quit()
                sys.exit()
            elif (event.type == KEYDOWN and event.key == K_ESCAPE):
                return
            else:
                
                global winner
                if winner=='x':
                    winplayer = x
                elif winner=='o':
                    winplayer = o 
                else:
                    font = pygame.font.Font('freesansbold.ttf',40)
                    winplayer = font.render("None",1, (128, 0, 66))       

                SCREEN.blit(home, (0,0))                
                wd =  pygame.image.load("gallery/board.png").convert_alpha()           
                win =  (pygame.transform.rotate(pygame.image.load("gallery/wins.png").convert_alpha(),-10))          
                font = pygame.font.Font('freesansbold.ttf',20)
                SCREEN.blit(font.render("-------------------------- ",1, (128, 0, 66)), (25,50))
                SCREEN.blit(font.render("__________",1, (128, 0, 66)), (220,50))
                SCREEN.blit(font.render("Tic-Toc-Toe",1, (128, 0, 66)), (220,50))
                SCREEN.blit(font.render("Game",1, (128, 0, 66)), (250,72))
                SCREEN.blit(font.render("------------------------------ ",1, (128, 0, 66)), (350,50))
                SCREEN.blit(font.render("Code by Omit",1, (0, 0, 66)), (SCREENWIDTH-210,SCREENHEIGHT-30))                
                SCREEN.blit(font.render("Press Esc for Mainscreen",True,white), (150,SCREENHEIGHT-80))  
                SCREEN.blit(x, (100,60))
                SCREEN.blit(o, (SCREENWIDTH/2+70,66))
                SCREEN.blit(versus, (230,85))
                SCREEN.blit(wd,(100,200))
                SCREEN.blit(winplayer, (140,240))
                SCREEN.blit(win, (250,220))
                font = pygame.font.Font('freesansbold.ttf',40)
                if winner != None:
                    SCREEN.blit(font.render("Congratulation!!!",1, (0, 0, 66)), (130,330))                
                else:
                    SCREEN.blit(font.render("Tie!!!",1, (0, 0, 66)), (180,330))                    
                pygame.display.update()        

def newgame():
    turn = pygame.image.load("gallery/turn.jpg").convert_alpha()           
    while flag:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx,my = pygame.mouse.get_pos()
                occupy_box(mx,my)
        SCREEN.blit(background, (0,0))
        SCREEN.blit(currentplayer,(250,0))
        SCREEN.blit(turn,(90,18))
        count = 0
        for point in BOXPOINT:        
            SCREEN.blit(box,point)
        for index in capture:    
            px,py = BOXPOINT[index]
            SCREEN.blit(capture_dict[index] , (px+25,py+25))
        
        pygame.display.update()   
        check_gameover()

if __name__ == "__main__":
    while True:    
        index()
        newgame()
        displayboard()    
