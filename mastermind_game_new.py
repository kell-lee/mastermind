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

class MasterMindGame():
    def __init__(self):
        self.marbles = []
        self.guesses = []
        self.code = self.secret_code()
        self.current_arrow = None
        self.round_num = 1
        self.marbles_dict = {}
        self.screen = turtle.Screen()
        self.check = turtle.Turtle()
        self.x_reset = turtle.Turtle()
        self.gif_button = turtle.Turtle()
        self.quit = turtle.Turtle()
        self.closed = False
        self.user = None
        self.t = turtle.Turtle()
        self.t.hideturtle()

    def hidden_pen(self):
        t = turtle.Turtle()
        
    def secret_code(self):
        colors = ["blue", "red", "green", "yellow", "purple", "black"]
        code = []
        NUM_COLORS = 4
    
        for i in range(NUM_COLORS):
            random_num = random.randint(0, len(colors) - 1)
            color = colors.pop(random_num)
            code.append(color)
        return code

    def username(self):
        
        while not self.user or self.user is None:
            self.user = turtle.textinput("CS5001 MasterMind", "Your Name:") 
        return self.user

    def log_errors(self, errors_file, error_type, date_time):
        with open(errors_file, mode="a") as outfile:
            error_str = f"On {date_time}, there was a {error_type}.\n"
            outfile.write(error_str)

    def create_file(self, leaderboard_file):
        try:
            open(leaderboard_file, "x")

        except FileExistsError:
            log_errors("mastermind_errors.err.txt", "FileNotFoundError",
                        datetime.datetime.now())

    def print_leaderboard(self, leaderboard_file):
        
        scores_dict = {}
        self.t.penup()
        self.t.goto(120, 400)
        self.t.pencolor("blue")

        outcome = self.win_or_lose()
        self.t.write("Leaders:", font=("Arial", 24, "normal"))
        try:
            with open(leaderboard_file, mode="r") as infile:
                for each in infile:
                    each = each.strip("\n")
                    each = each.replace(" ", "")
                    score, name = each.split(":")
                    if name not in scores_dict:
                        scores_dict[name] = score
                    else:
                        scores_dict[name] = min(scores_dict[name], score)

            if self.user not in scores_dict or self.round_num < \
               int(scores_dict[self.user]):
                if outcome:
                    scores_dict[self.user] = self.round_num

            sorted_scores = sorted(scores_dict.items(), key=lambda x:int(x[1]))

            if outcome:
                with open(leaderboard_file, mode="w") as outfile:
                    for name, score in sorted_scores:
                        outfile.write(f"{score}: {name}\n")

            if self.round_num == 1 and not outcome:
                i = 0
                for name, score in sorted_scores:
                    if i < 5:
                        self.t.goto(120, self.t.ycor() - 50)
                        self.t.write(f"{score}: {name}", font=("Arial", 18,
                                                          "normal"))
                        i += 1
                    else:
                        break
                    
        except FileNotFoundError:
            self.gif_button.goto(0, 0)
            self.gif_button.showturtle()
            self.gif_button.shape("leaderboard_error.gif")
            turtle.ontimer(lambda: self.gif_button.hideturtle(), 3000)
            self.log_errors("mastermind_errors.err.txt", "FileNotFoundError",
                            datetime.datetime.now())
            self.create_file(leaderboard_file)
        except PermissionError:
            self.log_errors("mastermind_errors.err.txt", "PermissionError",
                            datetime.datetime.now())

    def count_bulls_and_cows(self):
        bulls = 0
        cows = 0

        if len(self.guesses) != len(self.code):
            return (0, 0)
        for i in range(len(self.code)):
            if i < len(self.guesses):
                if self.guesses[i] == self.code[i]:
                    bulls += 1
                elif self.guesses[i] in self.code:
                    cows += 1
        return (bulls, cows)

    def draw_marbles(self, x_button_reset=False):
        x = 0
        y = 0
        
        if self.closed:
            return
        if self.screen is None or self.screen.getcanvas() is None:
            return
        for i in range(1, 11):
            if x_button_reset and i == self.round_num:
                for m in self.marbles_dict.get(i, []):
                    if not m.is_empty:
                        m.draw_empty()
            else:
                for j in range(4):
                    m = Marble(Point(-320 + x, 370 + y), "black", 20)
                    self.marbles_dict.setdefault(i, []).append(m)

                    if i == self.round_num:
                        if len(self.guesses) == 0:
                            m.draw_empty()
                        elif j < len(self.guesses):
                            m.color = self.guesses[j]
                            m.draw()
                    else:
                        m.draw_empty()
                    x += 60
                x = 0
                y -= 70

    def draw_side_marbles(self):
        (bulls, cows) = self.count_bulls_and_cows()
        x = 0
        y = 0
        
        if self.closed:
            return
        
        if self.screen is None or self.screen.getcanvas() is None:
            return
        for i in range(1, 11):
            marbles_colored = bulls + cows
            for j in range(4):
                if j % 2 == 0:
                    m = Marble(Point(-30 + x, 400 + y), "black", 5)

                    if i == self.round_num and marbles_colored > 0:
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
                    if i == self.round_num and marbles_colored > 0:
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
                    y -= 20
            y -= 30

    def guess_buttons(self):
        colors = ["blue", "red", "green", "yellow", "purple", "black"]
        x = 0
    
        for each in colors:
            m = Marble(Point(-350 + x, -390), each, 20)
            self.marbles.append(m)
            m.draw()
            x += 55

    def red_arrow(self):
        
        if 1 <= self.round_num <= 10:
            y_coordinate = 390 - (self.round_num - 1) *  70
            return Arrow(Point(-350, y_coordinate), "red")

    def check_guess(self, x, y):
        (bulls, cows) = self.count_bulls_and_cows()

        if len(self.guesses) != 4:
            return

        for each in self.marbles:
            each.draw()

        self.draw_side_marbles()
        outcome = self.win_or_lose()

        if not outcome:
            if self.round_num < 10:
                self.round_num += 1
                self.guesses.clear()

        if self.round_num > 1:
            if self.current_arrow:
                self.current_arrow.erase()
                self.current_arrow = self.red_arrow()
                self.current_arrow.draw()
                
        self.game_outcome()

    def check_button(self):
        
        self.check.speed(0)
        self.check.penup()
        self.check.goto(0, -380)
        self.check.shape("checkbutton.gif")

        if self.round_num == 1 and not self.current_arrow:
            self.current_arrow = self.red_arrow()
            self.current_arrow.draw()

        self.check.onclick(lambda x, y: self.check_guess(x, y))

    def reset(self):
        for each in self.marbles:
            if each.is_empty:
                each.draw()
        if self.guesses:
            self.guesses.clear()
            self.draw_marbles(True)
            
    def x_button(self):
        
        self.x_reset.speed(0)
        self.x_reset.penup()
        self.x_reset.goto(80, -380)
        self.x_reset.shape("xbutton.gif")

        self.x_reset.onclick(lambda x, y: self.reset())
    
    def game_outcome(self):
        (bulls, cows) = self.count_bulls_and_cows()
        
        if bulls == len(self.code):
            self.gif_button.shape("winner.gif")
            self.print_leaderboard("leaderboard.txt")
            self.closed = True
        elif self.round_num >= 10:
            self.gif_button.shape("Lose.gif")
            self.closed = True

    def win_or_lose(self):
        (bulls, cows) = self.count_bulls_and_cows()
        if bulls == len(self.code):
            self.closed = True
            return True
        elif self.round_num == 10:
            return False
        return False

    def quit_msg(self, x, y):
        
        self.gif_button.goto(0, 0)
        self.gif_button.shape("quitmsg.gif")
        self.closed = True

    def quit_button(self):
        
        self.quit.speed(0)
        self.quit.penup()
        self.quit.goto(300, -380)
        self.quit.shape("quit.gif")
        self.quit.onclick(lambda x,y: self.quit_msg(x, y))
        
    def window(self):
        if self.closed:
            return
        self.username()
        board = TurtleBoxes()
        board.left_box()
        board.right_box()
        board.bottom_box()
        self.quit_button()
        
    def click_guesses(self, x, y):
        if self.closed:
            return
        for each in self.marbles:
            if each.clicked_in_region(x, y):
                if not each.is_empty:
                    if len(self.guesses) < 4 and each.color not in self.guesses:
                        self.guesses.append(each.color)
                        each.draw_empty()
                        self.draw_marbles()

    def setup_clicks(self):
        turtle.onscreenclick(lambda x, y: self.click_guesses(x, y))
        
    def start_game(self):
        self.setup_clicks()
        while not self.closed:
            turtle.update()
            if self.closed:
                break
        
def main():
    
    game = MasterMindGame()
    
    print(game.code)

    game.window()
    game.print_leaderboard("leaderboard.txt")
    game.draw_marbles()
    game.draw_side_marbles()
    game.guess_buttons()
    game.check_button()
    game.x_button()
    
    game.start_game()
    turtle.bye()
    
if __name__ == "__main__":
    main()
    
