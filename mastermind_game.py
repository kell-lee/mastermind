"""
    Kelly Lee
    CS 5001, Fall 2023
    Project
"""
import turtle
import random
import time
import datetime
from Marble import Marble
from Point import Point
from Arrow import Arrow
from TurtleBoxes import TurtleBoxes

marbles = []
guesses = []
code = []
current_arrow = []
round_num = 1
marbles_dict = {}
user = None

def secret_code():
    global code
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

    lst = ["checkbutton.gif", "xbutton.gif", "quit.gif",
           "file_error.gif", "leaderboard_error.gif", "Lose.gif",
           "quitmsg.gif", "winner.gif"]
    
    for each in lst:
        s.register_shape(each) # registers gif files for use

def username():
    global user
    if user is None:
        user = turtle.textinput("CS5001 MasterMind", "Your Name:")
    return user
    
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

def log_errors(errors_file, error_type, date_time):
    with open(errors_file, mode="a") as outfile:
        error_str = f"On {date_time}, there was a {error_type}.\n"
        outfile.write(error_str)

def create_file(leaderboard_file):
    try:
        open(leaderboard_file, "x")

    except FileExistsError:
        log_errors("mastermind_errors.err.txt", "FileNotFoundError",
                    datetime.datetime.now())

def print_leaderboard(t, leaderboard_file, round_num, username):
    scores_dict = {}
    t.hideturtle()
    t.penup()
    t.goto(120,400)
    t.pencolor("blue")

    outcome = win_or_lose(round_num)
    t.write("Leaders:", font=("Arial", 24, "normal"))
    try:
        with open(leaderboard_file, mode="r") as infile:
            for each in infile:
                each = each.strip("\n")
                each = each.replace(" ", "")
                score, name = each.split(":")
                if name not in scores_dict:
                    scores_dict[name] = score
                # dictionary mapping name to score
                else:
                    scores_dict[name] = min(scores_dict[name], score)
                print(scores_dict)
        if username not in scores_dict or round_num < scores_dict[username]:
            if outcome:
                scores_dict[username] = round_num
    
        # sorts dictionary by value
        sorted_scores = sorted(scores_dict.items(), key=lambda x:x[1])
        print(sorted_scores)
        if outcome:
            with open(leaderboard_file, mode="w") as outfile:
                for name, score in sorted_scores:
                    outfile.write(f"{score}: {name}\n")
        if round_num == 1 and not outcome:
            i = 0
            for name, score in sorted_scores:
                if i < 5:
                    t.goto(120, t.ycor() - 50)
                    t.write(f"{score}: {name}",
                            font=("Arial", 18, "normal"))
                    i += 1
                else:
                    break
           
    except FileNotFoundError:
        t.goto(0, 0)
        t.showturtle()
        t.shape("leaderboard_error.gif")
        turtle.ontimer(lambda: t.hideturtle(), 3000)
        log_errors("mastermind_errors.err.txt", "FileNotFoundError",
                   datetime.datetime.now())
        create_file(leaderboard_file)
    except PermissionError:
        log_errors("mastermind_errors.err.txt", "PermissionError",
                   datetime.datetime.now())

def save_scores(t, leaderboard_file, round_num, username):
    scores_dict = {}
    outcome = game_outcome(round_num)
    
    try:
        with open(leaderboard_file, mode="r") as infile:
            for each in infile:
                each = each.strip("\n")
                if ":" in each:
                    score, name = each.split(":")
                    scores_dict[name.lower()] = int(score)
        if username.lower() not in scores_dict or \
           outcome < scores_dict[username]:
            if outcome:
                scores_dict[username] = round_num
        # sorts dictionary by value
        sorted_scores = sorted(scores_dict.items(), key=lambda x:x[1])

        with open(leaderboard_file, mode="w") as outfile:
            for name, score in sorted_scores:
                outfile.write(f"{score}: {name}\n")
    except FileNotFoundError:
        t.goto(0, 0)
        t.shape("leaderboard_error.gif")
        log_errors("mastermind_errors.err.txt", "FileNotFoundError",
                   datetime.datetime.now())
    except PermissionError:
        log_errors("mastermind_errors.err.txt", "PermissionError",
                   datetime.datetime.now())


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


def count_bulls_and_cows():
    global guesses
    global code
    bulls = 0 # correct position, black
    cows = 0 # correct color, red

    if len(guesses) != len(code):
        return (0, 0)
    for i in range(len(code)):
        if i < len(guesses):
            if guesses[i] == code[i]:
                bulls += 1
            elif guesses[i] in code:
                cows += 1
    return (bulls, cows)

def draw_marbles(round_num, x_button_reset=False):
    
    #global round_num
    global guesses
    global marbles_dict
   
    x = 0
    y = 0
    if turtle.Screen().getcanvas() is None:
        return
    for i in range(1, 11):
        if x_button_reset and i == round_num:
            for m in marbles_dict.get(i, []):
                if not m.is_empty:
                    m.draw_empty()
        else:
            for j in range(4):
                m = Marble(Point(-320 + x, 370 + y), "black", 20)
                marbles_dict.setdefault(i, []).append(m)
                if i == round_num:
                    if len(guesses) == 0:
                        m.draw_empty()
                    elif j < len(guesses):
                        m.color = guesses[j]
                        m.draw()
                else:
                    m.draw_empty()
            
                x += 60
            x = 0 # reset x to starting position
            y -= 70

def draw_side_marbles(round_num):
    (bulls, cows) = count_bulls_and_cows()
    y = 0
    x = 0
    if turtle.Screen().getcanvas() is None:
        return
    for i in range(1, 11):
        marbles_colored = bulls + cows
        for j in range(4):
            if j % 2 == 0: # if even:
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
                    
            else:
                n = Marble(Point(-30 + x + 15, 400 + y), "black", 5)
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
                y -= 20 # moves m and n down 20 
        y -= 30 # moves to next row of marbles
            
def guess_buttons():
    global marbles
    colors = ["blue", "red", "green", "yellow", "purple", "black"]
    x = 0
    
    for each in colors:
        m = Marble(Point(-350 + x, -390), each, 20)
        marbles.append(m)
        m.draw()
        x += 55


def red_arrow(round_num):
    if 1 <= round_num <= 10:
        y_coordinate = 390 - (round_num - 1) * 70
        return Arrow(Point(-350, y_coordinate), "red")
    

def check_guess(x, y):
    global round_num
    global guesses
    global code
    global current_arrow
    (bulls, cows) = count_bulls_and_cows()
    
    if len(guesses) != 4:
        return
    for each in marbles:
        each.draw()
        
    draw_side_marbles(round_num)
    outcome = win_or_lose(round_num)
    if not outcome:
        if round_num < 10:
            round_num += 1
            guesses.clear()

    
        if round_num > 1:
            if current_arrow:
                current_arrow.erase()
                current_arrow = red_arrow(round_num)
                current_arrow.draw()
    game_outcome(round_num)     

def check_button():
    global current_arrow
    t = turtle.Turtle()
    t.speed(0)
    t.penup()
    t.goto(0, -380)
    t.shape("checkbutton.gif")

    if round_num == 1 and not current_arrow:
        current_arrow = red_arrow(round_num)
        current_arrow.draw()
        
    t.onclick(check_guess)


    
def reset(x, y):
    print("Reset")
    global marbles
    global guesses
    global round_num
    
    for each in marbles:
        if each.is_empty:
            each.draw()
    if guesses:
        guesses.clear()
        print(guesses)
        draw_marbles(round_num, True)


def x_button():
   
    t = turtle.Turtle()
    t.speed(0)
    t.penup()
    t.goto(80, -380)
    t.shape("xbutton.gif")
    
    t.onclick(reset)
    
def game_outcome(round_num):
    (bulls, cows) = count_bulls_and_cows()
    global user
    t = turtle.Turtle()
    w = turtle.Turtle()
    if bulls == len(code):
        
        w.shape("winner.gif")
        w.getscreen().update()
        turtle.ontimer(turtle.bye, 3000) # closes window after 3 secs
        
    elif round_num > 10:
    
        w.shape("Lose.gif")
        w.getscreen().update()
        turtle.ontimer(turtle.bye, 3000)
       
    print_leaderboard(t, "leaderboard.txt", round_num, user)

def win_or_lose(round_num):
    (bulls, cows) = count_bulls_and_cows()
    if bulls == len(code):
        return True
    elif round_num == 10:
        return False
    return False

def quit_msg(x, y):
    q = turtle.Turtle()
    q.goto(0, 0)
    q.shape("quitmsg.gif")
    turtle.ontimer(turtle.bye, 3000)
    

def quit_button():
    t = turtle.Turtle()
    
    t.speed(0)
    t.penup()
    
    t.goto(300, -380)
    t.shape("quit.gif")

    t.onclick(quit_msg)


def window():
    #background_screen()
    username()
    #left_box()
    #right_box()
    #bottom_box()
    board = TurtleBoxes()
    board.left_box()
    board.right_box()
    board.bottom_box()
    quit_button()


def click_guesses(x,y):
    global guesses
    global marbles
    
    for each in marbles:
        if each.clicked_in_region(x,y):
            if not each.is_empty: 
                if len(guesses) < 4 and each.color not in guesses:
                    guesses.append(each.color)
                    each.draw_empty()
                    draw_marbles(round_num)
                                      
def main():
    t = turtle.Turtle()
    t.hideturtle()
    global user
    global round_num
    secret_code()
    print(code)
    print("---------\n")
    background_screen()
    
    window()
    print_leaderboard(t, "leaderboard.txt", round_num, user)
    draw_marbles(round_num)
    draw_side_marbles(round_num)
    guess_buttons()
    check_button()
    x_button()
    turtle.onscreenclick(click_guesses)
    #turtle.mainloop()
    

if __name__ == "__main__":
    main()
