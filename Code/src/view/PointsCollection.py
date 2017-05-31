from kivy.properties import NumericProperty

from view.Point import Point


class PointsCollection:
    # CONSTRUCTORS--------------------------------------------------------------
    def __init__(self, width, height, x_min, x_max, y_min, y_max):

        # ATTRIBUTES------------------------------------------------------------
        # Collection of points
        self.points_list = []

        # Window size
        self.graph_width = width
        self.graph_height = height

        # Boundaries
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

        # Increment
        self.x_increment = (self.graph_width) / (self.x_max - self.x_min)
        self.y_increment = (self.graph_height) / (self.y_max - self.y_min)

    # FACTORY METHODS-----------------------------------------------------------
    # GETTERS, SETTERS----------------------------------------------------------
    def get_points_list(self):
        return self.points_list

    # METHODS-------------------------------------------------------------------
    def add_point(self, point):
        if type(point) == Point:
            self.points_list.append(point)
        else:
            raise TypeError

    def add_point_vals(self, x_val, y_val):
        # Calculate position of point according to coordinate value
        x_pos = round(x_val * self.x_increment)
        y_pos = self.graph_height - round(y_val * self.y_increment)

        # Create new point
        new_point = Point(x_pos, y_pos, x_val, y_val)
        # new_point.x_pos = NumericProperty(x_pos)
        # new_point.y_pos = NumericProperty(y_pos)
        # new_point.x_value = x_val
        # new_point.y_value = y_val

        # Add point
        self.add_point(new_point)

    def remove_point(self, index):
        self.points_list.remove(index)

    def clear_list(self):
        self.points_list = []

        # HELPER FUNCTIONS----------------------------------------------------------
