"""Tkinter graphical interface for Connect Four."""
import tkinter as tk

from board import ROWS, COLS
from game import Game
from minimax_agent import MinimaxAgent

PAD = 18

BG, PANEL = "#0f172a", "#1e293b"
BOARD, BOARD_EDGE, HOLE = "#2563eb", "#1e40af", "#0f172a"
TEXT, MUTED, ACCENT = "#e2e8f0", "#94a3b8", "#38bdf8"
FILL = {1: "#ef4444", 2: "#facc15"}
RIM = {1: "#b91c1c", 2: "#ca8a04"}
DEPTHS = {"Easy": 2, "Medium": 4, "Hard": 7}
FONT = "Helvetica"


class App:
    def __init__(self, root):
        self.root = root
        root.title("Connect Four AI")
        root.configure(bg=BG)
        self.fullscreen = True
        try:
            root.attributes("-fullscreen", True)
        except tk.TclError:
            root.state("zoomed")
        root.bind("<F11>", lambda e: self._toggle_fullscreen())
        root.bind("<Escape>", lambda e: self._toggle_fullscreen(False))

        self.mode = tk.StringVar(value="ai")
        self.level = tk.StringVar(value="Medium")
        self.side = tk.IntVar(value=1) 
        self.scores = {1: 0, 2: 0, "draw": 0}
        self.session = 0
        self.busy = False
        self.hover = None
        self.anim = None
        self.agent = None
        self.cell, self.x0 = 60, PAD 

        self._build_ui()
        self.new_game()

    def _build_ui(self):
        tk.Label(self.root, text="CONNECT FOUR", bg=BG, fg=TEXT,
                 font=(FONT, 24, "bold")).pack(pady=(14, 0))
        tk.Label(self.root, text="Minimax  •  Alpha-Beta Pruning", bg=BG, fg=MUTED,
                 font=(FONT, 10)).pack(pady=(0, 8))

        panel = tk.Frame(self.root, bg=PANEL, padx=12, pady=10)
        panel.pack(fill="x", padx=PAD)
        self._segmented(panel, 0, "Mode", self.mode,
                        [("Human vs AI", "ai"), ("Human vs Human", "pvp")])
        self.level_row = self._segmented(panel, 1, "Difficulty", self.level,
                                         [(k, k) for k in DEPTHS])
        self.side_row = self._segmented(panel, 2, "You play", self.side,
                                        [("Red (first)", 1), ("Yellow (second)", 2)])
        tk.Button(panel, text="New Game", command=lambda: self.new_game(),
                  bg=ACCENT, fg=BG, activebackground="#7dd3fc", relief="flat",
                  font=(FONT, 11, "bold"), padx=14, pady=6, cursor="hand2"
                  ).grid(row=0, column=2, rowspan=3, padx=(16, 0), sticky="ns")
        panel.grid_columnconfigure(1, weight=1)

        self.status = tk.Label(self.root, text="", bg=BG, fg=TEXT, font=(FONT, 16, "bold"))
        self.status.pack(pady=(12, 2))

        self.canvas = tk.Canvas(self.root, width=300, height=300, bg=BG, highlightthickness=0)
        self.canvas.bind("<Configure>", self._on_resize)
        self.canvas.bind("<Motion>", self._on_motion)
        self.canvas.bind("<Leave>", lambda e: self._set_hover(None))
        self.canvas.bind("<Button-1>", self._on_click)
        for i in range(COLS):
            self.root.bind(str(i + 1), lambda e, c=i: self._human_move(c))
        self.root.bind("n", lambda e: self.new_game())

        tk.Label(self.root, text="Click a column or press 1–7  •  N: new game  •  Esc / F11: exit or enter fullscreen",
                 bg=BG, fg=MUTED, font=(FONT, 9)).pack(side="bottom", pady=(0, 10))
        score = tk.Frame(self.root, bg=BG)
        score.pack(side="bottom", pady=(4, 6))
        self.score_labels = {}
        for key in (1, "draw", 2):
            f = tk.Frame(score, bg=PANEL, padx=16, pady=6)
            f.pack(side="left", padx=6)
            dot = tk.Label(f, text="●", bg=PANEL, fg=FILL.get(key, MUTED), font=(FONT, 14))
            dot.pack(side="left")
            lbl = tk.Label(f, text="", bg=PANEL, fg=TEXT, font=(FONT, 11, "bold"))
            lbl.pack(side="left", padx=(4, 0))
            self.score_labels[key] = lbl
        self.canvas.pack(fill="both", expand=True, padx=PAD)

    def _segmented(self, parent, row, label, var, options):
        tk.Label(parent, text=label, bg=PANEL, fg=MUTED, font=(FONT, 10), width=9,
                 anchor="w").grid(row=row, column=0, pady=3, sticky="w")
        frame = tk.Frame(parent, bg=PANEL)
        frame.grid(row=row, column=1, sticky="w", pady=3)
        for text, value in options:
            tk.Radiobutton(frame, text=text, variable=var, value=value, indicatoron=0,
                           command=self._settings_changed, bg="#334155", fg=TEXT,
                           selectcolor=BOARD, activebackground=BOARD, activeforeground="white",
                           relief="flat", font=(FONT, 10), padx=10, pady=3, bd=0,
                           cursor="hand2").pack(side="left", padx=2)
        return frame

    def _toggle_fullscreen(self, value=None):
        self.fullscreen = (not self.fullscreen) if value is None else value
        try:
            self.root.attributes("-fullscreen", self.fullscreen)
        except tk.TclError:
            self.root.state("zoomed" if self.fullscreen else "normal")

    def _on_resize(self, e):
        """Fit the board to the available canvas area."""
        self.cell = max(30, min((e.width - 2 * PAD) // COLS, (e.height - PAD) // (ROWS + 1)))
        self.x0 = (e.width - COLS * self.cell) / 2
        self._draw()

    def _settings_changed(self):
        self.scores = {1: 0, 2: 0, "draw": 0}
        self.new_game()

    def _vs_ai(self):
        return self.mode.get() == "ai"

    def _ai_player(self):
        return 3 - self.side.get()

    def new_game(self):
        self.session += 1
        self.busy, self.anim = False, None
        self.game = Game()
        self.agent = MinimaxAgent(DEPTHS[self.level.get()]) if self._vs_ai() else None
        for row in (self.level_row, self.side_row):
            for w in row.winfo_children():
                w.configure(state="normal" if self._vs_ai() else "disabled")
        self._update_scores()
        self._update_status()
        self._draw()
        if self._ai_turn():
            self._schedule_ai()

    def _name(self, p):
        if self._vs_ai():
            return "You" if p == self.side.get() else "AI"
        return "Red" if p == 1 else "Yellow"

    def _ai_turn(self):
        return self._vs_ai() and not self.game.over and self.game.current == self._ai_player()

    def _human_move(self, col):
        if self.busy or self.game.over or self._ai_turn() or not self.game.board.is_legal(col):
            return
        self._play(col)

    def _play(self, col):
        self.busy = True
        player = self.game.current
        row = self.game.play(col)
        self._animate(col, row, player)

    def _after_move(self):
        self.busy = False
        if self.game.over:
            key = self.game.winner or "draw"
            self.scores[key] += 1
            self._update_scores()
        self._update_status()
        self._draw()
        if self._ai_turn():
            self._schedule_ai()

    def _schedule_ai(self):
        session = self.session
        self.busy = True
        self._update_status()
        self.root.after(350, lambda: self._ai_move(session))

    def _ai_move(self, session):
        if session != self.session:
            return
        col = self.agent.choose_move(self.game.board, self._ai_player())
        self._play(col)

    def _update_status(self):
        g = self.game
        if g.over:
            if g.winner:
                msg = {"You": "You win!", "AI": "The AI wins!"}.get(
                    self._name(g.winner), f"{self._name(g.winner)} wins!")
                color = FILL[g.winner]
            else:
                msg, color = "It's a draw!", TEXT
        elif self._ai_turn():
            msg, color = "AI is thinking…", FILL[g.current]
        elif self._vs_ai():
            msg, color = "Your turn", FILL[g.current]
        else:
            msg, color = f"{self._name(g.current)}'s turn", FILL[g.current]
        self.status.config(text=msg, fg=color)

    def _update_scores(self):
        self.score_labels[1].config(text=f"{self._name(1)}: {self.scores[1]}")
        self.score_labels[2].config(text=f"{self._name(2)}: {self.scores[2]}")
        self.score_labels["draw"].config(text=f"Draws: {self.scores['draw']}")

    def _col_at(self, x):
        col = int((x - self.x0) // self.cell)
        return col if 0 <= col < COLS else None

    def _on_motion(self, e):
        self._set_hover(self._col_at(e.x))

    def _set_hover(self, col):
        if col != self.hover:
            self.hover = col
            if not self.busy:
                self._draw()

    def _on_click(self, e):
        col = self._col_at(e.x)
        if col is not None:
            self._human_move(col)

    def _animate(self, col, row, player):
        target = row + 1.5                
        self.anim = {"col": col, "row": row, "player": player, "y": 0.5, "v": 0.0}
        session = self.session

        def step():
            if session != self.session or self.anim is None:
                return
            a = self.anim
            a["v"] += 0.026
            a["y"] += a["v"]
            if a["y"] >= target:
                self.anim = None
                self._after_move()
                return
            self._draw()
            self.root.after(14, step)

        step()

    def _disc(self, cx, cy, player, r=None):
        c = self.canvas
        r = r or self.cell * 0.4
        c.create_oval(cx - r, cy - r, cx + r, cy + r, fill=FILL[player], outline=RIM[player], width=3)
        r2 = r * 0.62
        c.create_oval(cx - r2, cy - r2, cx + r2, cy + r2, outline=RIM[player], width=2)

    def _draw(self):
        c, g = self.canvas, self.game
        CELL, TOP, X0 = self.cell, self.cell, self.x0
        c.delete("all")
        if (self.hover is not None and not self.busy and not g.over
                and not self._ai_turn() and g.board.is_legal(self.hover)):
            self._disc(X0 + self.hover * CELL + CELL / 2, TOP / 2, g.current)
        c.create_rectangle(X0 - 6, TOP - 6, X0 + COLS * CELL + 6, TOP + ROWS * CELL + 6,
                           fill=BOARD, outline=BOARD_EDGE, width=4)
        win = set(g.winning_cells)
        r = CELL * 0.4
        for row in range(ROWS):
            for col in range(COLS):
                cx, cy = X0 + col * CELL + CELL / 2, TOP + row * CELL + CELL / 2
                v = g.board.grid[row][col]
                if self.anim and (row, col) == (self.anim["row"], self.anim["col"]):
                    v = 0                   
                if v:
                    self._disc(cx, cy, v)
                else:
                    c.create_oval(cx - r, cy - r, cx + r, cy + r, fill=HOLE, outline=BOARD_EDGE, width=3)
                if (row, col) in win:
                    c.create_oval(cx - r - 4, cy - r - 4, cx + r + 4, cy + r + 4,
                                  outline="white", width=4)
        if self.anim:
            self._disc(X0 + self.anim["col"] * CELL + CELL / 2, self.anim["y"] * CELL, self.anim["player"])


def run():
    root = tk.Tk()
    App(root)
    root.mainloop()