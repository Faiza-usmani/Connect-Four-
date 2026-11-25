"""Minimax with Alpha-Beta Pruning and a heuristic evaluation."""
from agent import Agent
from board import ROWS, COLS

WIN_SCORE = 100_000
MOVE_ORDER = [3, 2, 4, 1, 5, 0, 6]


def _windows():
    wins = []
    for r in range(ROWS):
        for c in range(COLS):
            for dr, dc in [(0, 1), (1, 0), (1, 1), (1, -1)]:
                er, ec = r + 3 * dr, c + 3 * dc
                if 0 <= er < ROWS and 0 <= ec < COLS:
                    wins.append([(r + i * dr, c + i * dc) for i in range(4)])
    return wins


WINDOWS = _windows()


def evaluate(board, player):
    opp = 3 - player
    grid = board.grid
    score = 3 * sum(1 for r in range(ROWS) if grid[r][COLS // 2] == player) 
    for window in WINDOWS:
        mine = theirs = 0
        for r, c in window:
            v = grid[r][c]
            if v == player:
                mine += 1
            elif v == opp:
                theirs += 1
        if mine and theirs:
            continue                    
        if mine == 3:
            score += 5
        elif mine == 2:
            score += 2
        if theirs == 3:
            score -= 6      
        elif theirs == 2:
            score -= 2
    return score


class MinimaxAgent(Agent):
    def __init__(self, depth=4):
        self.depth = depth
        self.name = f"Minimax (depth {depth})"
        self.nodes = 0         

    def choose_move(self, board, player):
        self.nodes = 0
        self.player = player
        best_col, best_score = None, float("-inf")
        alpha, beta = float("-inf"), float("inf")
        for col in self._ordered(board):
            row = board.drop(col, player)
            if board.winning_line(row, col):
                score = WIN_SCORE + self.depth
            else:
                score = self._search(board, self.depth - 1, alpha, beta, False)
            board.undo()
            if score > best_score:
                best_col, best_score = col, score
            alpha = max(alpha, best_score)
        return best_col

    def _ordered(self, board):
        legal = set(board.legal_moves())
        return [c for c in MOVE_ORDER if c in legal]

    def _search(self, board, depth, alpha, beta, maximizing):
        self.nodes += 1
        moves = self._ordered(board)
        if not moves:
            return 0   
        if depth == 0:
            return evaluate(board, self.player)
        mover = self.player if maximizing else 3 - self.player
        best = float("-inf") if maximizing else float("inf")
        for col in moves:
            row = board.drop(col, mover)
            if board.winning_line(row, col):
                score = (WIN_SCORE + depth) if maximizing else -(WIN_SCORE + depth)
            else:
                score = self._search(board, depth - 1, alpha, beta, not maximizing)
            board.undo()
            if maximizing:
                best = max(best, score)
                alpha = max(alpha, best)
            else:
                best = min(best, score)
                beta = min(beta, best)
            if alpha >= beta:
                break             
        return best