import unittest
from board import Board, ROWS
from game import Game

DRAWN_GAME = [4, 3, 6, 0, 1, 4, 5, 5, 1, 1, 5, 0, 1, 6, 0, 1, 5, 5, 1, 0, 4, 6, 3, 2, 6, 6,
              0, 4, 6, 5, 2, 0, 4, 2, 4, 2, 2, 2, 3, 3, 3, 3]


class TestBoard(unittest.TestCase):
    def test_drop_stacks_from_bottom(self):
        b = Board()
        self.assertEqual(b.drop(3, 1), ROWS - 1)
        self.assertEqual(b.drop(3, 2), ROWS - 2)

    def test_full_column_is_illegal(self):
        b = Board()
        for i in range(ROWS):
            b.drop(0, 1 + i % 2)
        self.assertNotIn(0, b.legal_moves())
        with self.assertRaises(ValueError):
            b.drop(0, 1)

    def test_undo(self):
        b = Board()
        b.drop(2, 1)
        b.undo()
        self.assertEqual(b.heights[2], 0)
        self.assertEqual(b.grid[ROWS - 1][2], 0)

    def _play(self, cols):
        g = Game()
        for c in cols:
            g.play(c)
        return g

    def test_horizontal_win(self):
        self.assertEqual(self._play([0, 0, 1, 1, 2, 2, 3]).winner, 1)

    def test_vertical_win(self):
        self.assertEqual(self._play([0, 1, 0, 1, 0, 1, 0]).winner, 1)

    def test_diagonal_win(self):
        self.assertEqual(self._play([0, 1, 1, 2, 2, 3, 2, 3, 3, 6, 3]).winner, 1)

    def test_anti_diagonal_win(self):
        self.assertEqual(self._play([3, 2, 2, 1, 1, 6, 1, 0, 0, 0, 0]).winner, 1)

    def test_draw(self):
        g = self._play(DRAWN_GAME)
        self.assertTrue(g.over)
        self.assertTrue(g.is_draw)

    def test_no_moves_after_game_over(self):
        g = self._play([0, 0, 1, 1, 2, 2, 3])
        with self.assertRaises(ValueError):
            g.play(4)


if __name__ == "__main__":
    unittest.main()