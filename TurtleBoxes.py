"""
    Kelly Lee
    CS 5001, Fall 2023
    Project

    TurtleBoxes draws boxes and configures the background turtle screen.
"""
import turtle

PENSIZE = 10
S_WIDTH = 800 # screen width
S_HEIGHT = 1000 # screen height
ANGLE = 90 # angle to turn right or left
LEFT_WIDTH = 450 # left box width
BOX_HEIGHT = 750 # height of the boxes
LEFT_BOUND = -390 # left most x-coordinate 

class TurtleBoxes():
    """
    TurtleBoxes configures the drawings of the boxes needed for the
    MasterMindGame. It also sets the screen size and registers the
    shapes used in the game. 
    """
    def __init__(self, position=(0,0),color="black", size=PENSIZE):
        """
        Constructor -- __init__
            creates new instances of TurtleBoxes
        Parameters
            self -- current object
            position -- default is (0,0)
            color -- default is "black"
            size -- default is PENSIZE
        Returns
            None
        """
        self.pen = self.new_pen() 
        self.pen.hideturtle() # draw without turtle showing
        self.pen.speed(0)
        self.pen.pensize(size)
        self.color = color
        self.position = position
        self.set_screen() 

    def set_screen(self, title="CS5001 MasterMind Code Game",
                   width=S_WIDTH, height=S_HEIGHT):
        """
        Method -- set_screen
            sets up the screen size with the width and height, opens the
            screen window with the title, and registers shapes
        Parameters
            self -- current object
            title -- default is "CS5001 MasterMind Code Game"
            width -- deafult is S_WIDTH
            height -- default is S_HEIGHT
        Returns
            the screen s
        """
        s = turtle.Screen()
        s.title(title)
        s.setup(width, height)
        
        lst = ["checkbutton.gif", "xbutton.gif", "quit.gif",
               "file_error.gif", "leaderboard_error.gif", "Lose.gif",
               "quitmsg.gif", "winner.gif"]

        for each in lst:
            s.register_shape(each)
            
        return s
    
    def new_pen(self):
        """
        Method -- new_pen
            creates a new turtle object
        Parameters
            self -- current object
        Returns
            turtle.Turtle()   
        """
        return turtle.Turtle()

    def set_color(self, color):
        """
        Method -- set_color
            sets the pencolor
        Parameters
            self -- current object
            color -- color of pen
        Returns
            None
        """
        self.color = color
        self.pen.color(color)

    def left_box(self):
        """
        Method -- left_box
           draws the left_box with turtle object
        Parameters
            self -- current object
        Returns
            None  
        """
        self.pen.up() # does not draw
        self.pen.left(ANGLE)
        self.pen.goto(LEFT_BOUND, LEFT_WIDTH)
        self.pen.down() # will draw
        
        for i in range(2):
            self.pen.right(ANGLE)
            self.pen.forward(LEFT_WIDTH)
            self.pen.right(ANGLE)
            self.pen.forward(BOX_HEIGHT)
            
    def right_box(self):
        """
        Method -- right_box
            draws the right_box with turtle object
        Parameters
            self -- current object
        Returns
            None
        """
        RIGHT_WIDTH = 280
        RIGHT_BOUND = 100 # right most x-coordinate
        
        self.set_color("blue")
        self.pen.pensize(8)
        self.pen.up()
        self.pen.goto(RIGHT_BOUND, LEFT_WIDTH)
        self.pen.down()
        
        for i in range(2):
            self.pen.right(ANGLE)
            self.pen.forward(RIGHT_WIDTH)
            self.pen.right(ANGLE)
            self.pen.forward(BOX_HEIGHT)

    def bottom_box(self):
        """
        Method -- bottom_box
            draws the bottom_box with turtle object
        Parameters
            self -- current object
        Returns
            None
        """
        BOTTOM_WIDTH = 770
        BOTTOM_LENGTH = 120
        
        self.set_color("black")
        self.pen.up()
        
        # add by 10 to leave white space
        self.pen.goto(LEFT_BOUND, -LEFT_WIDTH + 10) 
        self.pen.down()
        
        for i in range(2):
            self.pen.forward(BOTTOM_LENGTH)
            self.pen.right(ANGLE)
            self.pen.forward(BOTTOM_WIDTH)
            self.pen.right(ANGLE)
    
def main():

    box = TurtleBoxes()
    box.left_box()
    box.right_box()
    box.bottom_box()
    
if __name__ == "__main__":
    main()
