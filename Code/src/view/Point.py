from kivy.app import App
from kivy.uix.widget import Widget
from kivy.vector import Vector

from kivy.properties import NumericProperty


class Point(Widget):
    def __init__(self, x_pos, y_pos, x_val, y_val):
        super(Point, self).__init__()
        self.x_pos = x_pos
        self.y_pos = y_pos

        self.pos = Vector(self.x_pos, self.y_pos)

        self.radius = 1
        self.size = Vector(self.radius, self.radius)

        self.x_value = x_val
        self.y_value = y_val
