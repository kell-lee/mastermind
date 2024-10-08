"""
    Kelly Lee
    CS 5001, Fall 2023
    Project
"""
import turtle
import random
import time
from Marble import Marble
from Point import Point


marbles = []
guesses = []
code = []
round_num = 1

def secret_code():
    colors = ["blue", "red", "green", "yellow", "purple", "black"]
   
    NUM_COLORS = 4
    code.clear()
    for i in range(NUM_COLORS):
        random_num = random.randint(0, len(colors) - 1)
        color = colors.pop(random_num)
        code.append(color)
   


def background_screen():
    s = turtle.Screen()
    s.title("CS5001 MasterMind Code Game")
    s.setup(width=800, height=1000)

    lst = ["checkbutton.gif", "xbutton.gif", "quit.gif", "lose.gif",
           "file_error.gif", "leaderboard_error.gif", "Lose.gif",
           "quitmsg.gif", "winner.gif"]
    def register(lst):
        for each in lst:
            s.register_shape(each) # registers gif files for use
    
    register(lst)

def left_box():
    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)
    
    t.penup()
    t.pensize(10)
    t.backward(390)
    t.left(90)
    t.forward(450)
    t.pendown()
    
    for i in range(2):
        t.right(90)
        t.forward(450)
        t.right(90)
        t.forward(750)

def right_box():
    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)
    
    t.pencolor("blue")
    t.pensize(8)
    t.penup()
    t.forward(100)
    t.left(90)
    t.forward(450)
    t.pendown()
    
    for i in range(2):
        t.right(90)
        t.forward(280)
        t.right(90)
        t.forward(750)
    
def bottom_box():
    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)
    
    t.penup()
    t.pensize(10)
    t.penup()
    t.backward(390)
    t.right(90)
    t.forward(320)
    t.pendown()

    for i in range(2):
        t.forward(120)
        t.left(90)
        t.forward(770)
        t.left(90)
    
    #t.register_shape("checkbutton.gif", (0, -370))
    #t.addshape("checkbutton.gif")

def username():
    user = turtle.textinput("CS5001 MasterMind", "Your Name:")
    return user

def draw_marbles():
    # m = Marble(Point(x, y), "black", 20)
    # m.draw_empty()
    i = 1
    x = 0
    y = 0

    while i <= 10:
        for j in range(4):
            m = Marble(Point(-320 + x, 370 + y), "black", 20)
            if i == round_num and j < len(guesses):
                m.color = guesses[j]
                m.draw()
            else:
                m.draw_empty()
            
            x += 60
        x = 0 # reset x to starting position
        y -= 70
        i += 1
        
def draw_side_marbles(round_num, bulls=0, cows=0):
    i = 1
    y = 0
    x = 0
    while i <= 10:
        if i == round_num:
            marbles_colored = bulls + cows
        for j in range(2):
            m = Marble(Point(-30 + x, 400 + y), "black", 5)
            if i == round_num and marbles_colored > 0:
                if bulls > 0:
                    m.color = "black"
                    bulls -= 1
                elif cows > 0:
                    m.color = "red"
                    cows -= 1
                m.draw()
                marbles_colored -= 1
            else:
                m.draw_empty()
         
            n = Marble(Point(-30 + x, 380 + y), "black", 5)
            if i == round_num and marbles_colored > 0:
                if bulls > 0:
                    n.color = "black"
                    bulls -= 1
                elif cows > 0:
                    n.color = "red"
                    cows -= 1
                n.draw()
                marbles_colored -= 1
            else:
                n.draw_empty()
                
            x += 15
        x = 0 
        y -= 70
        i += 1

def guess_buttons():
    colors = ["blue", "red", "green", "yellow", "purple", "black"]
    x = 0
    
    s = turtle.Screen()
    
    for each in colors:
        m = Marble(Point(-350 + x, -390), each, 20)
        m.draw()
        marbles.append(m)
        x += 55
 
def check_button():
    
    t = turtle.Turtle()
    t.speed(0)
    t.penup()
    t.goto(0, -380)
    t.shape("checkbutton.gif")

    
    def check_guess(x, y):
        global round_num
        global guesses
        print(guesses)
        bulls = 0 # correct position, black
        cows = 0 # correct color, red

        for each in marbles:
            each.draw()
        for i in range(len(code)):
            if guesses[i] == code[i]:
                bulls += 1
            elif guesses[i] in code:
                cows += 1
            
           
        draw_side_marbles(round_num, bulls, cows)
        round_num += 1
        
        guesses.clear()
        if bulls == len(code):
            t = turtle.Turtle()
            t.shape("winner.gif")

            turtle.exitonclick()
        
        
    t.onclick(check_guess)
    red_arrow(round_num)
    
def x_button():
    t = turtle.Turtle()
    t.speed(0)
    t.penup()
    t.goto(80, -380)
    t.shape("xbutton.gif")

    
    def reset(x, y):
        for each in marbles:
            each.draw()
        guesses = []

    t.onclick(reset)

def quit_button():
    t = turtle.Turtle()
    s = turtle.Screen()
    t.speed(0)
    t.penup()
    
    t.goto(300, -380)
    t.shape("quit.gif")
    q = turtle.Turtle()
    
    def quit_msg(x, y):
        q.goto(0, 0)
        q.shape("quitmsg.gif")
        turtle.exitonclick()
        
    t.onclick(quit_msg)
    

def red_arrow(round_num):
    t = turtle.Turtle()
    t.speed(0)
    t.pensize(10)
    t.penup()
    
    
    y_coordinate = 390 - (round_num - 1) * 70

    t.clear()
    turtle.update()
    
    t.goto(-350, y_coordinate)
    t.turtlesize(2, 2)
    t.fillcolor("red")

    return t
        
    
def window():
    background_screen()
    #username()
    left_box()
    right_box()
    bottom_box()
    quit_button()

def game_buttons():
    check_button()
    x_button()
    guess_buttons()
    red_arrow()

def click_guesses(x,y):
    #global round_num
    i = 1
    
   
    for each in marbles:
        if each.clicked_in_region(x,y):
            if not each.is_empty:
                color = each.color
                if color not in guesses and len(guesses) < 4:
                    guesses.append(color)
                    each.draw_empty()
                    draw_marbles()
                    turtle.update()
        if len(guesses) == 4:
            break


def main():
    #screen = turtle.Screen()
    secret_code()
    print(code)
    print("---------\n")
    window()
    draw_marbles()
    draw_side_marbles(round_num)
    
  
    while round_num <= 10:
        
        guess_buttons()
        check_button()
        x_button()
        
        turtle.onscreenclick(click_guesses)
        red_arrow(round_num)

    turtle.mainloop()

if __name__ == "__main__":
    main()
