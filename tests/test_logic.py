import unittest
from math import pi
from core import Frame, compare, sign
from game import GameModel
from entities import *


class LogicTest(unittest.TestCase):
    def test_intersection(self):
        frame1 = Frame(0, 0, 2, 2)
        frame2 = Frame(1, 1, 2, 2)
        self.assertTrue(frame1.intersects_with(frame2))

        frame1 = Frame(1, 1, 1, 1)
        frame2 = Frame(0, 0, 3, 3)
        self.assertTrue(frame1.intersects_with(frame2))

        frame1 = Frame(0, 1, 4, 2)
        frame2 = Frame(1, 0, 2, 4)
        self.assertTrue(frame1.intersects_with(frame2))

        frame1 = Frame(0, 0, 1, 4)
        frame2 = Frame(0, 5, 3, 1)
        self.assertFalse(frame1.intersects_with(frame2))

        frame1 = Frame(2, 2, 1, 1)
        frame2 = Frame(0, 0, 1, 1)
        self.assertFalse(frame1.intersects_with(frame2))

        frame1 = Frame(0, 0, 1, 1)
        frame2 = Frame(1, 1, 1, 1)
        self.assertTrue(frame1.intersects_with(frame2))

    def test_resizing(self):
        frame = Frame(0, 0, 20, 30).resize(10, 0)
        self.assertEqual(frame.width, 30)
        self.assertEqual(frame.height, 30)

    def test_relocation(self):
        frame = Frame(0, 0, 10, 10).relocate(10, 20)
        self.assertEqual(frame.x, 10)
        self.assertEqual(frame.y, 20)

    def test_transformation(self):
        frame = Frame(0, 0, 10, 10).transform(20, 30, 40, 50)
        self.assertEqual(frame.x, 20)
        self.assertEqual(frame.y, 30)
        self.assertEqual(frame.width, 50)
        self.assertEqual(frame.height, 60)

    def test_comparison(self):
        self.assertEqual(compare(1, 2), -1)
        self.assertEqual(compare(1, 1), 0)
        self.assertEqual(compare(2, 1), 1)

    def test_sign(self):
        self.assertEqual(sign(3), 1)
        self.assertEqual(sign(0), 0)
        self.assertEqual(sign(-100), -1)

    def test_ship_movement(self):
        ship = Ship(10, 500)
        ship.velocity = 10

        ship.move()
        self.assertEqual(ship.location, (20, 500))

        ship.move(0)
        self.assertEqual(ship.location, (20, 500))

        ship.velocity = 20
        ship.move(-1)
        self.assertEqual(ship.location, (0, 500))

    def test_ball_movement(self):
        ship = Ship(300, 1000)
        ball = Ball(350, 970)
        ball.change_state(BallState.Free)

        ball.direction = -pi / 2
        ball.velocity = 20

        ball.move()
        self.assertEqual(ball.location, (350, 950))

if __name__ == '__main__':
    unittest.main()
