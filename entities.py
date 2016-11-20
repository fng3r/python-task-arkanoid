import math
import os.path
import settings
from core import Frame, BallState, Vector


class Entity:
    def __init__(self, x, y, size):
        self.frame = Frame(x, y, *size)

    @property
    def x(self):
        return self.frame.x

    @property
    def y(self):
        return self.frame.y

    @property
    def width(self):
        return self.frame.width

    @property
    def height(self):
        return self.frame.height

    @property
    def top(self):
        return self.frame.top

    @property
    def bottom(self):
        return self.frame.bottom

    @property
    def middle(self):
        return self.frame.middle

    @property
    def left(self):
        return self.frame.left

    @property
    def right(self):
        return self.frame.right

    @property
    def center(self):
        return self.frame.center

    @property
    def location(self):
        return self.frame.location

    @location.setter
    def location(self, location):
        self.frame.location = location

    def intersects_with(self, other):
        return self.frame.intersects_with(other.frame)

    def resize(self, d_width, d_height):
        self.frame = self.frame.resize(d_width, d_height)

    def relocate(self, delta_x, delta_y):
        self.frame = self.frame.relocate(delta_x, delta_y)

    def transform(self, delta_x, delta_y, d_width, d_height):
        return self.relocate(delta_x, delta_y).resize(d_width, d_height)

    def get_image(self):
        return os.path.join('images', '%s.png' % type(self).__name__.lower())


class MovingEntity(Entity):
    def __init__(self, x, y, size, velocity, direction):
        super().__init__(x, y, size)
        self.velocity = velocity
        self.direction = Vector(*direction)

    def move(self, turn_rate=1):
        dir_angle = self.direction.angle
        delta_x = math.cos(dir_angle) * self.velocity * turn_rate
        delta_y = math.sin(dir_angle) * self.velocity * turn_rate
        self.frame = self.frame.relocate(delta_x, delta_y)


class Ship(MovingEntity):
    def __init__(self, x=0, y=0):
        super().__init__(x, y, settings.SHIP_SIZE, settings.SHIP_VELOCITY,
                         settings.SHIP_DIRECTION)
        self.bullets = 0

    def expand(self):
        self.frame = self.frame.transform(-self.frame.width / 2, 0,
                                          int(self.frame.width / 2), 0)

    def narrow(self):
        self.frame = self.frame.transform(self.frame.width / 2, 0,
                                          -int(self.frame.width / 2), 0)

    def get_ammo(self, count):
        self.bullets += count

    def try_shoot(self):
        if self.bullets > 0:
            self.bullets -= 2
            return True
        return False


class Ball(MovingEntity):
    def __init__(self, x=0, y=0):
        super().__init__(x, y, settings.BALL_SIZE, settings.BALL_VELOCITY,
                         settings.BALL_DIRECTION)
        self.state = BallState.Free
        self.was_reflected = False

    def stick_to_ship(self):
        self.change_state(BallState.Caught)

    def change_state(self, state):
        self.state = state

    def move(self, delta_x=None):
        if self.state != BallState.Caught:
            super().move()
        else:
            self.frame = self.frame.relocate(delta_x, 0)

    def accelerate(self):
        self.velocity = 1.5 * settings.BALL_VELOCITY

    def get_image(self):
        if self.state != BallState.Fiery:
            return super().get_image()
        else:
            return os.path.join('images', 'fireballbonus.png')


class Bullet(MovingEntity):
    def __init__(self, x, y):
        super().__init__(x, y, settings.BULLET_SIZE, settings.BULLET_VELOCITY,
                         settings.BULLET_DIRECTION)


class Brick(Entity):
    def __init__(self, x, y, color=None):
        super().__init__(x, y, settings.BRICK_SIZE)
        self.color = color
