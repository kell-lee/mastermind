"""
    Kelly Lee
    CS 5001, Fall 2023
    Project

    Turtle Window
"""
import turtle

PENSIZE = 10
WIDTH = 800
HEIGHT = 1000
ANGLE = 90
LEFT_WIDTH = 450
LEFT_HEIGHT = 750

class Background():
    def __init__(self, width=WIDTH, height=HEIGHT):
        self.width = width

    def set_screen(self, width=WIDTH, height=HEIGHT):
        self.width = width
        self.height = height
        return turtle.Screen()


class TurtleBoxes():
    def __init__(self, position=(0,0),color="black", size=PENSIZE):
        self.pen = self.new_pen()
        self.pen.hideturtle()
        self.pen.speed(0)
        self.pen.pensize(size)
        self.color = color
        self.position = position
        

    def set_screen(self, width=WIDTH, height=HEIGHT):
        self.width = width
        self.height = height
        return turtle.Screen().setup(width, height)
    
    def new_pen(self):
        return turtle.Turtle()

    def set_color(self, color):
        self.color = color

    def left_box(self):
        self.pen.up()
        self.pen.left(ANGLE)
        self.pen.goto(self.position[0], self.position[1])
        self.pen.down()
        for i in range(2):
            self.pen.right(ANGLE)
            self.pen.forward(LEFT_WIDTH)
            self.pen.right(ANGLE)
            self.pen.forward(LEFT_HEIGHT)

def main():
   
    
    box = TurtleBoxes(position=(-390, 450))
    box.set_screen()
    box.left_box()
if __name__ == "__main__":
    main()
