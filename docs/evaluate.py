"""Evaluate the Minimax agent against the random baseline. """
import argparse
import csv
import os
import random
import time

from board import Board
from game import Game
from minimax_agent import MinimaxAgent
from random_agent import RandomAgent

OUT = "results"


def play_game(agents):
    game = Game()
    while not game.over:
        game.play(agents[game.current].choose_move(game.board, game.current))
    return game.winner


def run_config(depth, games, seed):
    wins = draws = losses = 0
    nodes = elapsed = moves = 0
    for i in range(games):
        ai, rnd = MinimaxAgent(depth), RandomAgent(seed + i)
        ai_player = 1 if i % 2 == 0 else 2
        agents = {ai_player: ai, 3 - ai_player: rnd}

        game = Game()
        while not game.over:
            agent = agents[game.current]
            t = time.perf_counter()
            col = agent.choose_move(game.board, game.current)
            if agent is ai:
                elapsed += time.perf_counter() - t
                nodes += ai.nodes
                moves += 1
            game.play(col)
        if game.winner == ai_player:
            wins += 1
        elif game.winner == 0:
            draws += 1
        else:
            losses += 1
    return dict(depth=depth, games=games, wins=wins, draws=draws, losses=losses,
                avg_nodes=round(nodes / moves), avg_time_ms=round(1000 * elapsed / moves, 2))


def _random_position(rng):
    game = Game()
    for _ in range(rng.randint(4, 24)):
        if game.over:
            break
        game.play(rng.choice(game.board.legal_moves()))
    return game


def _wins_now(board, col, player):
    row = board.drop(col, player)
    won = bool(board.winning_line(row, col))
    board.undo()
    return won


def tactical_accuracy(depth, positions=100, seed=7):
    rng = random.Random(seed)
    agent = MinimaxAgent(depth)
    win_ok = win_n = block_ok = block_n = 0
    attempts = 0
    while (win_n < positions or block_n < positions) and attempts < 200_000:
        attempts += 1
        game = _random_position(rng)
        if game.over:
            continue
        b, me = game.board, game.current
        my_wins = [c for c in b.legal_moves() if _wins_now(b, c, me)]
        their_wins = [c for c in b.legal_moves() if _wins_now(b, c, 3 - me)]
        if my_wins and win_n < positions:
            win_n += 1
            win_ok += agent.choose_move(b, me) in my_wins
        elif len(their_wins) == 1 and not my_wins and block_n < positions:
            block_n += 1
            block_ok += agent.choose_move(b, me) == their_wins[0]
    return (win_ok / max(win_n, 1), block_ok / max(block_n, 1))


def make_charts(rows):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not installed - skipping charts (pip install matplotlib)")
        return
    d = [str(r["depth"]) for r in rows]
    g = [r["games"] for r in rows]

    fig, ax = plt.subplots(figsize=(7, 4))
    for key, color in (("wins", "#22c55e"), ("draws", "#94a3b8"), ("losses", "#ef4444")):
        ax.plot(d, [100 * r[key] / r["games"] for r in rows], marker="o", label=key.title(), color=color)
    ax.set(xlabel="Search depth", ylabel="Rate (%)", title="Minimax vs Random: Win/Draw/Loss rate")
    ax.legend(); ax.grid(alpha=.3)
    fig.tight_layout(); fig.savefig(f"{OUT}/win_rate.png", dpi=150); plt.close(fig)

    fig, ax1 = plt.subplots(figsize=(7, 4))
    ax1.bar(d, [r["avg_nodes"] for r in rows], color="#38bdf8")
    ax1.set(xlabel="Search depth", ylabel="Avg nodes per move", yscale="log",
            title="Search effort and decision time")
    ax2 = ax1.twinx()
    ax2.plot(d, [r["avg_time_ms"] for r in rows], color="#f97316", marker="o")
    ax2.set_ylabel("Avg decision time (ms)", color="#f97316")
    fig.tight_layout(); fig.savefig(f"{OUT}/nodes_and_time.png", dpi=150); plt.close(fig)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--games", type=int, default=100)
    p.add_argument("--depths", type=int, nargs="+", default=[1, 2, 3, 4, 5])
    p.add_argument("--seed", type=int, default=42)
    a = p.parse_args()

    os.makedirs(OUT, exist_ok=True)
    print(f"Seed={a.seed}, games per depth={a.games}\n")
    print(f"{'Depth':>5} {'W':>4} {'D':>4} {'L':>4} {'Nodes/move':>11} {'ms/move':>9} {'Win-take':>9} {'Block':>7}")
    rows = []
    for depth in a.depths:
        r = run_config(depth, a.games, a.seed)
        r["win_taking"], r["blocking"] = tactical_accuracy(depth, seed=a.seed)
        rows.append(r)
        print(f"{depth:>5} {r['wins']:>4} {r['draws']:>4} {r['losses']:>4} {r['avg_nodes']:>11} "
              f"{r['avg_time_ms']:>9} {r['win_taking']:>8.0%} {r['blocking']:>7.0%}")

    with open(f"{OUT}/results.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader(); w.writerows(rows)
    make_charts(rows)
    print(f"\nSaved results to {OUT}/")


if __name__ == "__main__":
    main()