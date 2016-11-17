import settings
from entities import Brick


class Level:
    def __init__(self, lvl, blocks):
        self.lvl = lvl
        self.blocks = blocks


class LevelCreator:
    @staticmethod
    def get_levels(game_size):
        levels = {}
        w_num = 10
        h_num = 11
        level = 1
        width = (game_size.width - w_num * settings.brick_size.width) / 2
        height = 50

        blocks = set()
        for i in range(h_num):
            for j in range(w_num):
                if i % 2 == 0 or j == 0 or j == 9:
                    blocks.add(LevelCreator._create_block(width, height, i, j))

        levels[level] = Level(level, blocks)

        level = 2
        height = 50
        blocks = set()
        for i in range(11):
            for j in range(i % 2, 11, 2):
                blocks.add(LevelCreator._create_block(width, height, i, j))

        levels[level] = Level(level, blocks)

        level = 3
        height = 100
        blocks = set()
        for i in range(10):
            for j in range(10):
                blocks.add(LevelCreator._create_block(width, height, i, j))

        levels[level] = Level(level, blocks)
        return levels

    @staticmethod
    def _create_block(width, height, i, j):
        block_location = LevelCreator._get_block_location(width, height, i, j)
        return Brick(*block_location)

    @staticmethod
    def _get_block_location(width, height, i, j):
        block_x = width + settings.brick_size.width * j
        block_y = height + settings.brick_size.height * i
        return block_x, block_y
