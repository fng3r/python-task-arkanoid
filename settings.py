import math
from core import Size

ball_size = Size(32, 32)
ship_size = Size(190, 30)
bonus_size = Size(25, 25)
brick_size = Size(90, 20)
bullet_size = Size(10, 18)

ball_velocity = 15
ship_velocity = 30
bonus_velocity = 15
bullet_velocity = 20

ball_direction = -math.pi / 4
ship_direction = 0
bonus_direction = math.pi / 2
bullet_direction = -math.pi / 2
