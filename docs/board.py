"""Board representation and Connect Four rules."""

ROWS, COLS = 6, 7
EMPTY = 0
DIRECTIONS = [(0, 1), (1, 0), (1, 1), (1, -1)]  


class Board:
    def __init__(self):
        self.grid = [[EMPTY] * COLS for _ in range(ROWS)]
        self.heights = [0] * COLS      
        self.moves = []              

    def legal_moves(self):
        return [c for c in range(COLS) if self.heights[c] < ROWS]

    def is_legal(self, col):
        return 0 <= col < COLS and self.heights[col] < ROWS

    def drop(self, col, player):
        if not self.is_legal(col):
            raise ValueError(f"Column {col} is full or invalid")
        row = ROWS - 1 - self.heights[col]
        self.grid[row][col] = player
        self.heights[col] += 1
        self.moves.append((row, col, player))
        return row

    def undo(self):
        row, col, _ = self.moves.pop()
        self.grid[row][col] = EMPTY
        self.heights[col] -= 1

    def is_full(self):
        return len(self.moves) == ROWS * COLS

    def winning_line(self, row, col):
        player = self.grid[row][col]
        if player == EMPTY:
            return []
        for dr, dc in DIRECTIONS:
            cells = [(row, col)]
            for sign in (1, -1):
                r, c = row + sign * dr, col + sign * dc
                while 0 <= r < ROWS and 0 <= c < COLS and self.grid[r][c] == player:
                    cells.append((r, c))
                    r, c = r + sign * dr, c + sign * dc
            if len(cells) >= 4:
                return cells
        return []

    def copy(self):
        b = Board()
        b.grid = [row[:] for row in self.grid]
        b.heights = self.heights[:]
        b.moves = self.moves[:]
        return b

    def __str__(self):
        sym = {0: ".", 1: "X", 2: "O"}
        return "\n".join(" ".join(sym[v] for v in row) for row in self.grid)