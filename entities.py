import math
import os.path
import settings
from core import Frame, BallState


class Entity:
    def __init__(self, x, y, size):
        self.frame = Frame(x, y, *size)

    @property
    def location(self):
        return self.frame.location

    def get_image(self):
        return os.path.join('images', '%s.png' % type(self).__name__.lower())


class MovingEntity(Entity):
    def __init__(self, x, y, size, velocity=0, direction=0):
        super().__init__(x, y, size)
        self.velocity = velocity
        self.direction = direction

    def move(self, turn_rate=1):
        delta_x = int(math.cos(self.direction) * self.velocity * turn_rate)
        delta_y = int(math.sin(self.direction) * self.velocity * turn_rate)
        self.frame = self.frame.relocate(delta_x, delta_y)


class Ship(MovingEntity):
    def __init__(self, x, y):
        super().__init__(x, y, settings.ship_size, settings.ship_velocity,
                         settings.ship_direction)
        self.bullets = 0

    def expand(self):
        self.frame = self.frame.transform(-self.frame.width / 2, 0,
                                          int(self.frame.width / 2), 0)

    def narrow(self):
        self.frame = self.frame.transform(self.frame.width / 2, 0,
                          -int(self.frame.width / 2), 0)

    def get_ammo(self, count):
        self.bullets += count


class Ball(MovingEntity):
    def __init__(self, x, y):
        super().__init__(x, y, settings.ball_size, settings.ball_velocity,
                         settings.ball_direction)
        self.state = BallState.Free

    def stick_to_ship(self):
        self.change_state(BallState.Caught)

    def change_state(self, state):
        self.state = state

    def move(self, delta_x=None):
        if self.state != BallState.Caught:
            super().move()
        else:
            self.frame = self.frame.relocate(delta_x)

    def accelerate(self):
        self.velocity = 1.5 * settings.ball_velocity

    def get_image(self):
        if self.state != BallState.Fiery:
            return super().get_image()
        else:
            return os.path.join('images', 'fireballbonus.png')


class Bullet(MovingEntity):
    def __init__(self, x, y):
        super().__init__(x, y, settings.bullet_size, settings.bullet_velocity,
                         settings.bullet_direction)


class Brick(Entity):
    def __init__(self, x, y, color=None):
        super().__init__(x, y, settings.brick_size)
        self.color = color
