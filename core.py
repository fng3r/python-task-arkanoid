import math
from collections import namedtuple
from enum import Enum


Size = namedtuple('Size', ['width', 'height'])


class Frame:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    @property
    def top(self):
        return self.y

    @property
    def bottom(self):
        return self.y + self.height

    @property
    def middle(self):
        return self.bottom - int(self.height / 2)

    @property
    def left(self):
        return self.x

    @property
    def right(self):
        return self.x + self.width

    @property
    def location(self):
        return self.x, self.y

    @location.setter
    def location(self, location):
        self.x, self.y = location

    def intersects_with(self, frame):
        return min(self.right, frame.right) >= max(self.left, frame.left) and\
            min(self.bottom, frame.bottom) >= max(self.top, frame.top)

    def resize(self, d_width=0, d_height=0):
        return Frame(self.x, self.y,
                     self.width + d_width, self.height + d_height)

    def relocate(self, delta_x=0, delta_y=0):
        return Frame(self.x + delta_x, self.y + delta_y,
                     self.width, self.height)

    def transform(self, delta_x, delta_y, d_width, d_height):
        return self.relocate(delta_x, delta_y).resize(d_width, d_height)

    def __str__(self):
        return '(%s, %s), width: %s, height: %s' % (self.x, self.y, self.width,
                                                    self.height)


class BallState(Enum):
    Caught = 0
    Free = 1
    Fiery = 2


def compare(one, other):
    if one < other:
        return -1
    else:
        return int(one > other)


def sign(number):
    if number == 0:
        return number
    return int(math.copysign(1, number))
