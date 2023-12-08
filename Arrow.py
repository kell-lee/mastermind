"""
    Kelly Lee
    CS 5001, Fall 2023
    Project

    Arrow handles the arrow that moves to indicate the round (row) of game.
"""
import turtle
from Point import Point

ARROW_SIZE = 10

class Arrow:
    """
    Arrow manages the movement of the turtle arrow within the MasterMindGame
    by moving and pointing to the current row of marbles.
    """
    def __init__(self, position, color, size = ARROW_SIZE):
        """
        Constructor -- __init__
            creates new instances of Arrow
        Parameters
            self -- current object
            position -- (x,y) position of turtle
            color -- color of turtle
            size -- size of turtle arrow
        """
        self.pen = self.new_pen()
        self.color = color
        self.size = size
        self.position = position
        self.visible = False
        self.pen.speed(0)
        
    def new_pen(self):
        """
        Method -- new_pen
            creates a new turtle object
        Parameters
            self -- current_object
        Returns
            turtle.Turtle()
        """
        return turtle.Turtle()

    def draw(self):
        """
        Method -- draw
            draws the turtle arrow
        Parameters
            self -- current_object
        Returns
            None
        """
        self.pen.up() # doesn't draw
        self.pen.goto(self.position.x, self.position.y) # move to position
        self.visible = True
        self.pen.down() # draws
        self.pen.shapesize(2, 2) # makes turtle head bigger
        self.pen.fillcolor(self.color)
        self.pen.begin_fill()
        self.pen.end_fill()

    def erase(self):
        """ 
        Method -- erase
            hides turtle so it "erases"
        Parameters
            self -- current object
        Returns
            None
        """
        self.pen.hideturtle()
        self.visible = False

def main():
    arrow = Arrow(Point(100, 100), "red")
    arrow.draw()
    arrow.erase()

if __name__ == "__main__":
    main()
    
