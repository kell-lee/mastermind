"""
    Kelly Lee
    CS 5001, Fall 2023
    Project

    MasterMindGame
"""

import turtle
import random
import datetime
from Marble import Marble
from Point import Point
from Arrow import Arrow
from TurtleBoxes import TurtleBoxes

class MasterMindGame():
    """
    MasterMindGame represents tha main game logic, board drawings,
    and the click actions.
    """
    def __init__(self):
        """
        Constructor -- __init__
            creates a new instance of MasterMindGame
        Parameters
            self -- current object
        Returns
            None
        """
        self.marbles = [] # store marbles in the bottom row
        self.guesses = []
        
        self.code = self.secret_code()
        self.round_num = 1 # keep track of round_num
        
        # initialize marbles_dict which maps round_num to marble objects
        self.marbles_dict = {}
        
        self.screen = turtle.Screen()
        self.check = self.hidden_pen()
        self.x_reset = self.hidden_pen()
        self.gif_button = self.hidden_pen()
        self.quit = self.hidden_pen()
        self.t = self.hidden_pen()
        
        self.closed = False # window is not closed
        self.user = None
        self.current_arrow = None
        
    def hidden_pen(self):
        """
        Method -- hidden_pen
            creates a new turtle object that is hidden
        Parameters
            self -- current object
        Returns
            turtle.Turtle()
        """
        t = turtle.Turtle()
        t.speed(0)
        t.hideturtle()
        return t
        
    def secret_code(self):
        """
        Method -- secret_code
            creates the secret code using random
        Parameters
            self -- current object
        Returns
            code which is a list 
        """
        colors = ["blue", "red", "green", "yellow", "purple", "black"]
        code = []
        NUM_COLORS = 4
    
        for i in range(NUM_COLORS):
            random_num = random.randint(0, len(colors) - 1)
            color = colors.pop(random_num)
            code.append(color)
        return code

    def username(self):
        """
        Method -- username
            asks for username input from the user using turtle dialog window
        Parameters
            self -- current object
        Returns
            self.user 
        """
        while not self.user or self.user is None:
            self.user = turtle.textinput("CS5001 MasterMind", "Your Name:") 
        return self.user

    def log_errors(self, errors_file, error_type, date_time):
        """
        Method -- log_errors
            writes errors in the errors_file
        Parameters
            self -- current object
            errors_file -- file where errors will be logged
            error_type -- string that says type of error
            date_time -- date and time that error occurred
        Returns
            None
        """
        with open(errors_file, mode="a") as outfile:
            error_str = f"On {date_time}, there was a {error_type}.\n"
            outfile.write(error_str)

    def create_file(self, leaderboard_file):
        """
        Method -- create_file
            creates file if file does not exist
        Parameters
            self -- current object
            leaderboard_file -- file
        Returns
            None
        """
        try:
            open(leaderboard_file, "x")

        except FileExistsError:
            log_errors("mastermind_errors.err.txt", "FileNotFoundError",
                        datetime.datetime.now())

    def read_file(self, leaderboard_file):
        """
        Method -- read_file
            reads files for the leaderboard scores and create a dictionary
            that maps name to best score if there are multiple scores that
            a user has
        Parameters
            self -- current object
            leaderboard_file -- file
        Returns
            scores_dict which maps name to score
        """
        SECS = 3000 # milliseconds delay
        scores_dict = {}
        
        try:
            with open(leaderboard_file, mode="r") as infile:
                for each in infile:
                    each = each.strip("\n")
                    each = each.replace(" ", "")
                    score, name = each.split(":")
                    if name not in scores_dict:
                        scores_dict[name] = score
                    # takes best score of user which is the lowest number
                    else:
                        scores_dict[name] = min(scores_dict[name], score)
        except FileNotFoundError:
            self.gif_button.showturtle()
            self.gif_button.shape("leaderboard_error.gif")
            turtle.ontimer(lambda: self.gif_button.hideturtle(), SECS)
            self.log_errors("mastermind_errors.err.txt", "FileNotFoundError",
                            datetime.datetime.now())
            self.create_file(leaderboard_file)
        except PermissionError:
            self.log_errors("mastermind_errors.err.txt", "PermissionError",
                            datetime.datetime.now())
        return scores_dict

    def write_scores(self, sorted_scores):
        """
        Method -- write_scores
            writes the scores on the turtle screen
        
        """
        X_COOR = 120 # start at this x-coordinate to write score
        Y_COOR = 400 # start at this y-coordinate to write score
        SIZE = 24
        SCORE_SIZE = 18
        
        self.t.penup()
        self.t.goto(X_COOR, Y_COOR)
        self.t.pencolor("blue")
        self.t.write("Leaders:", font=("Arial", SIZE, "normal"))
        i = 0 # initialize i
        for name, score in sorted_scores:
            if i < 5: # prints top 5
                # subtract by 50 to leave whitespace
                self.t.goto(X_COOR, self.t.ycor() - 50) 
                self.t.write(f"{score}: {name}", font=("Arial",
                                                       SCORE_SIZE, "normal"))
                i += 1
            else:
                break
                        
    def print_leaderboard(self, leaderboard_file):
        """
        Method -- print_leaderboard
            sorts the scores to print the best score on top and logs
            player's results in leaderboard_file
        Parameters
            self -- current object
            leaderboard_file -- file
        Returns
            None
        """
        outcome = self.win_or_lose() # if True, then player won
        scores_dict = self.read_file(leaderboard_file)

        # if new player, or their new score is better, add to dictionary
        if self.user not in scores_dict or \
           self.round_num < int(scores_dict[self.user]):
                if outcome:
                    scores_dict[self.user] = self.round_num

        sorted_scores = sorted(scores_dict.items(), key=lambda x:int(x[1]))

        if outcome:
            with open(leaderboard_file, mode="w") as outfile:
                for name, score in sorted_scores:
                    outfile.write(f"{score}: {name}\n")

        # prints leaderboard in the beginning
        if self.round_num == 1 and not outcome:
            self.write_scores(sorted_scores)
 
    def count_bulls_and_cows(self):
        """
        Method -- count_bulls_and_cows
            counts correct position and color (bulls) and incorrect position
            and correct color (cows)
        Parameters
            self -- current object
        Returns
            (bulls, cows) which is a tuple
        """
        bulls = 0
        cows = 0

        # checks to make sure there are four guesses
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
        """
        Method -- draw_marbles
            draws 10 rows of 4 marbles and displays current and previous
            guesses in the game
        Parameters
            self -- current object
            x_button_reset -- a boolean to check if the x_button_reset
            was clicked
        """
        x = 0
        y = 0
        X_COOR = -320
        Y_COOR = 370
        #if self.screen is None or self.screen.getcanvas() is None:
            #return
        for i in range(1, 11):
            if x_button_reset and i == self.round_num:
                for m in self.marbles_dict.get(i, []):
                    if not m.is_empty: # clear marble colors
                        m.draw_empty()
            else:
                for j in range(4):
                    m = Marble(Point(X_COOR + x, Y_COOR + y), "black", 20)
                    self.marbles_dict.setdefault(i, []).append(m)
                    
                    if i == self.round_num:
                        if len(self.guesses) == 0:
                            m.draw_empty()
                        elif j < len(self.guesses):
                            # color marbles according to guesses
                            m.color = self.guesses[j]
                            m.draw()
                    else:
                        m.draw_empty()
                    x += 60 # space marbles by 60
                x = 0 # reset x back to 0 to start at same place for each row
                y -= 70 # space each row by 70

    def draw_side_marbles(self):
        """
        Method -- draw_side_marbles
            
        """
        (bulls, cows) = self.count_bulls_and_cows()
        x = 0
        y = 0
        
        
        #if self.screen is None or self.screen.getcanvas() is None:
            #return
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
        
        
        self.check.penup()
        self.check.goto(0, -380)
        self.check.showturtle()
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
        
        self.x_reset.penup()
        self.x_reset.goto(80, -380)
        self.x_reset.showturtle()
        self.x_reset.shape("xbutton.gif")

        self.x_reset.onclick(lambda x, y: self.reset())
    
    def game_outcome(self):
        (bulls, cows) = self.count_bulls_and_cows()
        
        if bulls == len(self.code):
            
            self.gif_button.shape("winner.gif")
            self.gif_button.showturtle()
            self.print_leaderboard("leaderboard.txt")
            self.closed = True
        elif self.round_num >= 10:

            self.gif_button.shape("Lose.gif")
            self.gif_button.showturtle()
            self.gif_button.textinput("Secret Code Was", f"{self.code}")
            self.closed = True

    def win_or_lose(self):
        (bulls, cows) = self.count_bulls_and_cows()
        if bulls == len(self.code):
            self.closed = True
            return True
        elif self.round_num == 10:
            self.closed = True
            return False
        return False

    def quit_msg(self, x, y):
        
        self.gif_button.showturtle()
        self.gif_button.shape("quitmsg.gif")
        self.closed = True

    def quit_button(self):
        
        self.quit.penup()
        self.quit.goto(300, -380)
        self.quit.showturtle()
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
        turtle.hideturtle()
        
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
    
