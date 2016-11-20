import random
from math import pi, cos
import settings
from bonuses import Bonus
from entities import Ship, Ball, Bullet
from core import Frame, BallState, Vector
from level import LevelCreator


class Player:
    def __init__(self):
        self.score = 0
        self.lives = 3

    def gain_life(self):
        self.lives += 1

    def die(self):
        self.lives -= 1

    def get_scores(self, blocks_count):
        self.score += 30 * blocks_count


class GameModel:
    def __init__(self, size):
        self.size = size
        self.frame = Frame(0, 0, *size)

        self.player = Player()
        self.current_level = 1

        self.won = False
        self.reset()
        self.deadly_height = self.ship.bottom - \
            self.ship.frame.height / 2

        self.levels = LevelCreator.get_levels(size)
        self.level = self.levels[self.current_level]

        self.bonuses = set()
        self.bullets = set()

    @property
    def gameover(self):
        return self.player.lives == 0

    @property
    def level_completed(self):
        return len(self.level.blocks) == 0

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
        if self.ball.state == BallState.Caught:
            self.ball.change_state(BallState.Free)
            return True
        return False

    def shooting(self):
        if self.ship.try_shoot():
            bullet1 = Bullet(self.ship.left, self.ship.top)
            bullet2 = Bullet(self.ship.right, self.ship.top)
            self.bullets.add(bullet1)
            self.bullets.add(bullet2)

    def tick(self, turn_rate=0):
        if self.gameover or self.won:
            return

        old_x = self.ship.left
        self.ship.move(turn_rate)
        self.normalize_ship_location()
        self.ball.move(self.ship.left - old_x)
        self.try_reflect_ball()

        if self.ball.middle > self.deadly_height:
            self.kill_player()

        if self.level_completed:
            self.player.score += 1000 * self.current_level
            if not self.try_get_next_level():
                self.won = True

        blocks_to_remove = {block for block in self.level.blocks
                            if block.intersects_with(self.ball)}
        if len(blocks_to_remove) != 0:
            self.smash_blocks(blocks_to_remove)

        self.remove_bonuses()
        self.remove_bullets()

        if self.ball.intersects_with(self.ship):
            mid = self.ship.right - self.ship.width / 2
            ball_mid = self.ball.right - self.ball.width / 2
            self.ball.direction = Vector.from_angle(
                -pi / 2 + (pi / 2.75 * (ball_mid - mid) /
                           (self.ship.width / 2)))

    def try_get_next_level(self):
        self.current_level += 1
        if self.current_level < len(self.levels) + 1:
            self.level = self.levels[self.current_level]
            self.reset()
            return True
        return False

    def kill_player(self):
        self.player.die()
        self.reset()

    def reset(self):
        self.bonuses = set()
        self.bullets = set()

        self.ship = Ship((self.size.width - settings.SHIP_SIZE.width) / 2,
                         self.size.height - settings.SHIP_SIZE.height)

        ball_x = self.ship.x + (self.ship.width -
                                settings.BALL_SIZE.width) / 2
        ball_y = self.ship.top - settings.BALL_SIZE.height
        self.ball = Ball(ball_x, ball_y)
        self.ball.stick_to_ship()

    def normalize_ship_location(self):
        self.ship.location = (min(max(0, self.ship.left),
                                  self.frame.right - self.ship.width),
                              self.ship.y)

    def try_reflect_ball(self):
        ball = self.ball
        if ball.direction.x > 0 and ball.right > self.frame.right or \
                ball.direction.x < 0 and ball.x < self.frame.left:
            ball.direction.x = -ball.direction.x

        if ball.direction.y < 0 and ball.y < self.frame.top + 0.1:
            ball.direction.y = -ball.direction.y

    def try_get_bonus(self, block):
        chance = random.random()
        if chance > 0.75:
            bonus_cls = Bonus.get_random_bonus()
            bonus = bonus_cls(block.left, block.top)
            self.bonuses.add(bonus)

    def smash_blocks(self, blocks_to_remove):
        block = next(iter(blocks_to_remove))
        if self.ball.state != BallState.Fiery:
            ball = self.ball
            delta = ball.center - block.center
            ball.direction.normalize()

            if abs(delta.x) - ball.velocity * abs(cos(ball.direction.x)) <= \
                    block.width / 2:
                ball.direction.y = -ball.direction.y
            else:
                ball.direction.x = -ball.direction.x
        self.level.blocks -= blocks_to_remove

        self.try_get_bonus(block)
        self.player.get_scores(len(blocks_to_remove))

    def remove_bonuses(self):
        bonuses_to_remove = {bonus for bonus in self.bonuses
                             if not bonus.intersects_with(self)}
        for bonus in self.bonuses:
            bonus.move()
            if bonus.intersects_with(self.ship):
                bonus.activate(self)
                bonuses_to_remove.add(bonus)

        self.bonuses -= bonuses_to_remove

    def remove_bullets(self):
        bullets_to_remove = {bullet for bullet in self.bullets
                             if not bullet.intersects_with(self)}
        blocks_to_remove = set()
        for bullet in self.bullets:
            bullet.move()
            for block in self.level.blocks:
                if bullet.intersects_with(block):
                    blocks_to_remove.add(block)
                    bullets_to_remove.add(bullet)

        self.bullets -= bullets_to_remove
        self.level.blocks -= blocks_to_remove
