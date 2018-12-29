import unittest

from BallClass import Ball


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(False, False)

    def test_try_move(self):
        from main import try_move
        from BallClass import Ball
        balls = [Ball(0, 0, "red"), Ball(0, 1, "red"), Ball(1, 0, "red"), Ball(1, 1, "red")]
        self.assertFalse(try_move([(197, 19), (400, 19)], balls))

    def test_not_try_move(self):
        from main import try_move
        from BallClass import Ball
        balls = [Ball(0, 0, "red"), Ball(0, 1, "red"), Ball(1, 1, "red")]
        self.assertTrue(try_move([(197, 19), (400, 19)], balls))

    def test_no_lines(self):
        from main import find_lines
        from BallClass import Ball
        from FieldClass import Field
        field = Field("record.txt")
        field.balls = [Ball(0, 0, "red")]
        find_lines(field)
        print(len(field.balls))
        self.assertEquals(len(field.balls), 1)

    def test_ball_constructor(self):
        from BallClass import Ball
        ball = Ball(1, 2, "red")
        self.assertEquals(ball.X, 1)
        self.assertEquals(ball.Y, 2)
        self.assertEquals(ball.Color, "red")

    def test_field_constructor(self):
        from FieldClass import Field
        text = open("record.txt", 'r')
        best_score = int(text.readlines()[0])
        field = Field("record.txt")
        self.assertEquals(len(field.Balls), 3)
        self.assertEquals(field.Score, 0)
        self.assertEquals(field.BestScore, best_score)

    def test_one_line(self):
        from main import find_lines
        from BallClass import Ball
        from FieldClass import Field
        field = Field("record.txt")
        field.Balls = [Ball(0, 0, "red"), Ball(1, 0, "red"), Ball(2, 0, "red"), Ball(3, 0, "red"), Ball(4, 0, "red"), Ball(5, 0, "red")]
        find_lines(field)
        self.assertEquals(len(field.Balls), 0)

    def test_one_love(self):
        from main import find_lines
        from BallClass import Ball
        from FieldClass import Field
        field = Field("record.txt")
        field.Balls = [Ball(0, 0, "red"), Ball(0, 1, "red"), Ball(0, 2, "red"), Ball(0, 3, "red"), Ball(0, 4, "red"), Ball(0, 6, "red")]
        find_lines(field)
        self.assertEquals(len(field.Balls), 1)

    def test_one_love(self):
        from main import find_lines
        from BallClass import Ball
        from FieldClass import Field
        field = Field("record.txt")
        field.Balls = [Ball(0, 0, "red"), Ball(0, 1, "red"), Ball(0, 2, "red"), Ball(0, 3, "red"), Ball(0, 4, "red"), Ball(0, 6, "red")]
        find_lines(field)
        self.assertEquals(len(field.Balls), 1)

    def test_get_position(self):
        from main import get_position
        self.assertEquals(get_position(0, 100), (-4, 2))

    def test_load_and_upload(self):
        from main import make_preservation
        from main import load_preservation
        from FieldClass import Field
        field = Field("record.txt")
        field.Balls = [Ball(0, 0, "red"), Ball(0, 1, "red"), Ball(0, 2, "red"), Ball(0, 3, "red"), Ball(0, 4, "red"),
                       Ball(0, 6, "red")]
        make_preservation(field)
        field.Balls.clear()
        load_preservation(field)
        self.assertEquals(len(field.Balls), 6)


if __name__ == '__main__':
    unittest.main()
