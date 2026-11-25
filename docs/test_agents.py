import unittest
from board import Board
from minimax_agent import MinimaxAgent
from random_agent import RandomAgent


def setup(p1_cols, p2_cols):
    b = Board()
    for c in p1_cols:
        b.drop(c, 1)
    for c in p2_cols:
        b.drop(c, 2)
    return b


class TestAgents(unittest.TestCase):
    def test_random_agent_only_plays_legal_moves(self):
        b, agent = Board(), RandomAgent(seed=1)
        for _ in range(6):
            b.drop(0, 1)
        for _ in range(50):
            self.assertIn(agent.choose_move(b, 1), b.legal_moves())

    def test_takes_immediate_win(self):
        b = setup([0, 1, 2], [0, 1, 2])    
        for depth in (1, 2, 4):
            self.assertEqual(MinimaxAgent(depth).choose_move(b, 1), 3)

    def test_blocks_immediate_loss(self):
        b = Board()
        for c in (0, 1, 2):
            b.drop(c, 2) 
        b.drop(6, 1)
        for depth in (2, 3, 4):
            self.assertEqual(MinimaxAgent(depth).choose_move(b, 1), 3)

    def test_pruning_visits_fewer_nodes_with_less_depth(self):
        b = Board()
        a2, a4 = MinimaxAgent(2), MinimaxAgent(4)
        a2.choose_move(b, 1)
        a4.choose_move(b, 1)
        self.assertLess(a2.nodes, a4.nodes)

    def test_prefers_centre_on_empty_board(self):
        self.assertEqual(MinimaxAgent(4).choose_move(Board(), 1), 3)

    def test_board_unchanged_after_search(self):
        b = setup([3, 3], [2, 4])
        before = [row[:] for row in b.grid]
        MinimaxAgent(4).choose_move(b, 1)
        self.assertEqual(b.grid, before)


if __name__ == "__main__":
    unittest.main()