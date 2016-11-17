import random
from math import pi
import settings
from bonuses import Bonus
from entities import Ship, Ball, Bullet
from core import Frame, BallState, compare, sign
from level import LevelCreator


class GameModel:
    def __init__(self, size):
        self.size = size
        self.frame = Frame(0, 0, *size)

        self.gameover = False
        self.lives = 3
        self.current_level = 1
        self.scores = 0

        self.reset()
        self.deadly_height = self.ship.frame.bottom - \
            self.ship.frame.height / 2

        self.levels = LevelCreator.get_levels(size)
        self.level = self.levels[self.current_level]

        self.bonuses = set()
        self.bullets = set()

    def get_entities(self):
        yield self.ship
        yield self.ball
        for block in self.level.blocks:
            yield block
        for bullet in self.bullets:
            yield bullet
        for bonus in self.bonuses:
            yield bonus

    def release_ball(self):
        self.ball.state = BallState.Free

    def shooting(self):
        if self.ship.bullets > 0:
            self.ship.bullets -= 2
            bullet1 = Bullet(self.ship.frame.left, self.ship.frame.top)
            bullet2 = Bullet(self.ship.frame.right, self.ship.frame.top)
            self.bullets.add(bullet1)
            self.bullets.add(bullet2)

    def tick(self, turn_rate):
        if self.gameover:
            return

        if self.lives == 0:
            self.gameover = True
            return

        old_x = self.ship.frame.x
        self.ship.move(turn_rate)
        self.normalize_ship_location()
        self.ball.move(self.ship.frame.x - old_x)
        self.try_reflect_ball()

        if self.ball.frame.middle > self.deadly_height:
            self.lives -= 1
            self.reset()

        if len(self.level.blocks) == 0:
            self.scores += 1000 * self.current_level
            self.try_get_next_level()

        blocks_to_remove = {block for block in self.level.blocks
                            if block.frame.intersects_with(self.ball.frame)}
        if len(blocks_to_remove) != 0:
            block = next(iter(blocks_to_remove))
            if self.ball.state != BallState.Fiery:
                if not (self.ball.frame.right <= block.frame.right and
                        self.ball.frame.left >= block.frame.left):
                    self.ball.direction = sign(self.ball.direction) * \
                        pi - self.ball.direction
                elif self.ball.frame.top < block.frame.bottom < \
                        self.ball.frame.bottom:
                    self.ball.direction = -compare(self.ball.frame.top,
                                                   block.frame.top) * \
                        self.ball.direction
                elif block.frame.top < self.ball.frame.bottom < \
                        block.frame.bottom:
                    self.ball.direction = \
                        compare(self.ball.frame.bottom, block.frame.bottom) *\
                        self.ball.direction

            chance = random.random()
            if chance > 0.75:
                bonus_cls = Bonus.get_random_bonus()
                bonus = bonus_cls(block.frame.x, block.frame.y)
                self.bonuses.add(bonus)

        self.scores += 30 * len(blocks_to_remove)

        bonuses_to_remove = {bonus for bonus in self.bonuses
                             if not(bonus.frame.intersects_with(self.frame))}
        for bonus in self.bonuses:
            bonus.move()
            if bonus.frame.intersects_with(self.ship.frame):
                bonus.activate(self)
                bonuses_to_remove.add(bonus)

        self.bonuses -= bonuses_to_remove

        bullets_to_remove = {bullet for bullet in self.bullets
                             if not(bullet.frame.intersects_with(self.frame))}
        for bullet in self.bullets:
            bullet.move()
            for block in self.level.blocks:
                if bullet.frame.intersects_with(block.frame):
                    blocks_to_remove.add(block)
                    bullets_to_remove.add(bullet)

        self.level.blocks -= blocks_to_remove
        self.bullets -= bullets_to_remove

        if self.ball.frame.intersects_with(self.ship.frame):
            mid = self.ship.frame.right - self.ship.frame.width / 2
            self.ball.direction = -pi / 2 + (pi / 2 *
                                             (self.ball.frame.x - mid) /
                                             (self.ship.frame.width / 2))

    def try_get_next_level(self):
        self.current_level += 1
        if self.current_level < len(self.levels) + 1:
            self.level = self.levels[self.current_level]
            self.reset()
            return True
        return False

    def reset(self):
        self.bonuses = set()
        self.bullets = set()

        self.ship = Ship(int((self.size.width - settings.ship_size.width) / 2),
                         self.size.height - settings.ship_size.height)

        ball_x = self.ship.frame.x + int((self.ship.frame.width -
                                          settings.ball_size.width) / 2)
        ball_y = self.ship.frame.top - settings.ball_size.height
        self.ball = Ball(ball_x, ball_y)
        self.ball.stick_to_ship()

    def normalize_ship_location(self):
        self.ship.frame.location = (min(max(0, self.ship.frame.left),
                                        self.frame.right -
                                        self.ship.frame.width),
                                    self.ship.frame.y)

    def try_reflect_ball(self):
        if self.ball.frame.top <= self.frame.top:
            self.ball.direction = -self.ball.direction
        elif self.ball.frame.right >= self.frame.right or \
                self.ball.frame.left <= self.frame.left:
            self.ball.direction = sign(self.ball.direction) *\
                pi - self.ball.direction
