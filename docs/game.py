"""Turn management and game flow."""
from board import Board


class Game:
    def __init__(self, first_player=1):
        self.board = Board()
        self.current = first_player
        self.winner = 0
        self.winning_cells = []
        self.over = False

    def play(self, col):
        if self.over:
            raise ValueError("Game is over")
        row = self.board.drop(col, self.current)
        cells = self.board.winning_line(row, col)
        if cells:
            self.winner, self.winning_cells, self.over = self.current, cells, True
        elif self.board.is_full():
            self.over = True        
        else:
            self.current = 3 - self.current
        return row

    @property
    def is_draw(self):
        return self.over and self.winner == 0
