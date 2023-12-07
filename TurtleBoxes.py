"""
    Kelly Lee
    CS 5001, Fall 2023
    Project

    Turtle Window
"""
import turtle

PENSIZE = 10
S_WIDTH = 800 # screen width
S_HEIGHT = 1000 # screen height
ANGLE = 90
LEFT_WIDTH = 450
BOX_HEIGHT = 750
LEFT_BOUND = -390 # left most x-coordinate 

class TurtleBoxes():
    def __init__(self, position=(0,0),color="black", size=PENSIZE):
        self.pen = self.new_pen()
        self.pen.hideturtle()
        self.pen.speed(0)
        self.pen.pensize(size)
        self.color = color
        self.position = position
        self.set_screen()

    def set_screen(self, title="CS5001 MasterMind Code Game",
                   width=S_WIDTH, height=S_HEIGHT):
        
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
        return turtle.Turtle()

    def set_color(self, color):
        self.color = color
        self.pen.color(color)

    def left_box(self):
        self.pen.up()
        self.pen.left(ANGLE)
        # access position x, y using indexing
        self.pen.goto(LEFT_BOUND, LEFT_WIDTH)
        self.pen.down()
        for i in range(2):
            self.pen.right(ANGLE)
            self.pen.forward(LEFT_WIDTH)
            self.pen.right(ANGLE)
            self.pen.forward(BOX_HEIGHT)
            
    def right_box(self):
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
