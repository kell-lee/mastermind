import turtle
from Point import Point

ARROW_SIZE = 10

class Arrow:
    def __init__(self, position, color, size = ARROW_SIZE):
        self.pen = self.new_pen()
        self.color = color
        self.size = size
        #self.pen.hideturtle()
        self.position = position
        self.visible = False
        self.pen.speed(0)
        

    def new_pen(self):
        
        return turtle.Turtle()

    def draw(self):
        self.pen.up()
        #y_coordinate = 390 - (round_num - 1) * 70
        #X_COORDINATE = -350
        self.pen.goto(self.position.x, self.position.y)
        self.visible = True
        self.pen.down()
        self.pen.shapesize(2, 2)
        self.pen.fillcolor(self.color)
        self.pen.begin_fill()
        self.pen.end_fill()

    def erase(self):
        self.pen.hideturtle()
        self.visible = False

def main():
    arrow = Arrow(Point(100, 100), "red")
    arrow.draw()
    arrow.erase()


if __name__ == "__main__":
    main()
    
