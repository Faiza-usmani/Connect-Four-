"""Random-move baseline."""
import random
from agent import Agent


class RandomAgent(Agent):
    name = "Random"

    def __init__(self, seed=None):
        self.rng = random.Random(seed)
        self.nodes = 0

    def choose_move(self, board, player):
        return self.rng.choice(board.legal_moves())
