import random
import settings
from entities import MovingEntity
from core import BallState


class Bonus(MovingEntity):
    def __init__(self, x, y):
        super().__init__(x, y, settings.BONUS_SIZE, settings.BONUS_VELOCITY,
                         settings.BONUS_DIRECTION)

    def activate(self, game):
        pass

    @staticmethod
    def get_random_bonus():
        return BONUSES[random.randint(0, len(BONUSES) - 1)]


class DecreaseBonus(Bonus):
    def __init__(self, x, y):
        super().__init__(x, y)

    def activate(self, game):
        game.ship.narrow()


class ExpandBonus(Bonus):
    def __init__(self, x, y):
        super().__init__(x, y)

    def activate(self, game):
        game.ship.expand()


class BulletBonus(Bonus):
    def __init__(self, x, y):
        super().__init__(x, y)

    def activate(self, game):
        game.ship.get_ammo(12)


class FireBallBonus(Bonus):
    def __init__(self, x, y):
        super().__init__(x, y)

    def activate(self, game):
        game.ball.change_state(BallState.Fiery)


class FastBallBonus(Bonus):
    def __init__(self, x, y):
        super().__init__(x, y)

    def activate(self, game):
        game.ball.accelerate()


class LifeBonus(Bonus):
    def __init__(self, x, y):
        super().__init__(x, y)

    def activate(self, game):
        game.player.gain_life()


class DeathBonus(Bonus):
    def __init__(self, x, y):
        super().__init__(x, y)

    def activate(self, game):
        game.kill_player()


BONUSES = [DecreaseBonus, ExpandBonus, BulletBonus, FireBallBonus,
           FastBallBonus, LifeBonus, DeathBonus]
