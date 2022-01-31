#turtle gaming

import turtle
import math
import random
# import playsound
import time

#set up screen
#wn=turtle.Turtle()
wn=turtle.Screen()
wn.setup(width=1366,height=768)
wn = turtle.Screen()
wn.bgcolor("black")
wn.bgpic("kbgame-bg.gif")
wn.tracer(2)


#draw border
my = turtle.Turtle()
my.color("white")
my.penup()
my.setposition(-300,-300)
my.pendown()
my.pensize(3)
for side in range(4):
    my.forward(600)
    my.left(90)
my.hideturtle()

#create plaer turtle
player = turtle.Turtle()
player.color("blue")
player.shape("turtle")
player.penup() 
player.speed(0)

#create score
score = 0

#ceating 
maxGoals = 10
goal1 = []

for count in range(maxGoals):
    goal1.append(turtle.Turtle())
    goal1[count].color("green")
    goal1[count].shape("circle")
    goal1[count].penup()
    goal1[count].speed(0)
    goal1[count].setposition(random.randint(-290,290), random.randint(-290, 290))

#create goal
 

#set speed  varaiable   
speed = 1
#define funs
def turnleft():
    player.left(30) 

def turnright():
    player.right(30)

def increasespeed():
    global speed
    speed += 1

def decreasespeed():
    global speed
    speed-=1

def isCollision(t1, t2):
    d = math.sqrt(math.pow(t1.xcor() - t2.xcor(),2) + math.pow(t1.ycor() - t2.ycor(),2))
    if d < 20:
        return True
    else:
        return False

 #set keyboard bindings
turtle.listen()
turtle.onkey(turnleft,"Left")
turtle.onkey(turnright,"Right")
turtle.onkey(increasespeed,"Up")
turtle.onkey(decreasespeed,"Down")


while True:
    player.forward(speed)
#move to goal
    for count in range(maxGoals):
        goal1[count].forward(3)

        #boundary checking
        if goal1[count].xcor() > 290 or goal1[count].xcor() <- 290:
            
            goal1[count].right(180)
    #boundary checking
        if goal1[count].ycor() > 290 or goal1[count].ycor() <- 290:
            
            goal1[count].right(180)

        if isCollision(player, goal1[count]):
       
            goal1[count].setposition(random.randint(-290, 290),random.randint(-290, 290))
            goal1[count].right(random.randint(0,360))
            score += 1
            #drea 
            my.undo()
            my.penup()
            my.hideturtle()
            my.setposition(-290, 320)
            scorestring = "Score : %s" %score
            my.write(scorestring, False, align="left", font= ("Arial", 14, "bold italic"))

#boundary checking if out of boundary game over
    if player.xcor() > 301 or player.xcor() <- 301 or player.ycor() > 301 or player.ycor() <- 301:
        time.sleep(1)
        wn.clear()
        wn.bgcolor("black")
        my.goto(-250,-70)
        my.write("Game over",align="left", font= ("Helvetica", 80, "bold italic"))
        time.sleep(2)
        exit()

turtle.done()


