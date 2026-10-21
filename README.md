# Connect Four AI 🎮

An AI-powered Connect Four game developed as a semester project for **AL-2002: Artificial Intelligence Laboratory, Fall 2026**, at FAST-NUCES, Karachi Campus.

The project combines a graphical game interface with adversarial search algorithms to demonstrate how Artificial Intelligence can make strategic decisions in a competitive environment.

## 📌 Project Overview

Connect Four is a two-player strategy game played on a **6 × 7 grid**. Players take turns dropping their colored pieces into columns, aiming to connect four pieces horizontally, vertically, or diagonally.

This project allows players to play against another human or a computer-controlled opponent. The AI uses the **Minimax algorithm with Alpha-Beta Pruning** and heuristic evaluation to select strategic moves, recognize threats, and improve its chances of winning.

## ✨ Features

- **Human vs. Human:** Play against another player on the same device.
- **Human vs. AI:** Challenge a computer-controlled opponent.
- **Minimax Algorithm:** Evaluate possible future moves to select strategic actions.
- **Alpha-Beta Pruning:** Reduce unnecessary search by skipping branches that cannot affect the final decision.
- **Heuristic Evaluation:** Assess board positions based on center-column control, potential winning patterns, and opponent threats.
- **Difficulty Selection:** Adjust the AI's search depth.
- **Win and Draw Detection:** Identify winning combinations and drawn games.
- **Restart Game:** Start a new game whenever desired.
- **Random AI Baseline:** Compare the strategic AI against an opponent that selects legal moves randomly.

## 🧠 AI Techniques

### 1. Minimax Algorithm
Explores possible future game states by considering the AI's moves and the opponent's responses. The AI selects the move with the best expected outcome within the configured search depth.

### 2. Alpha-Beta Pruning
Optimizes Minimax by eliminating branches that cannot influence the final decision, allowing the AI to search more efficiently.

### 3. Heuristic Evaluation
Assigns scores to non-terminal board states using factors such as:
- Center-column preference.
- Two-piece and three-piece patterns in four-cell windows.
- Opportunities to complete four pieces in a row.
- Penalties for potential opponent winning patterns.
- Preference for earlier wins and delayed losses.

### 4. Random Move Baseline
Selects uniformly from the currently legal columns and serves as a baseline for evaluating the strategic AI.

## 🛠️ Technologies

- **Programming Language:** Python
- **AI Algorithms:** Minimax and Alpha-Beta Pruning
- **GUI:** Python-based graphical interface
- **Data:** Locally generated Connect Four board states and test scenarios
- **Version Control:** Git and GitHub

*Note: Specific GUI libraries and additional dependencies will be documented once finalized.*

## 🎯 Project Objectives

- Implement the standard rules of Connect Four.
- Develop a strategic AI opponent using adversarial search.
- Improve search efficiency through Alpha-Beta Pruning.
- Provide an interactive graphical interface.
- Evaluate AI performance against a random-move baseline.
- Analyze the relationship between search depth, decision time, and AI performance.

## 📊 Evaluation

The AI will be evaluated through repeated matches against the random-move baseline under consistent game conditions.

The evaluation will measure:

- **Win/Draw/Loss Rates:** Assess the AI's overall performance.
- **Average Nodes Evaluated:** Measure search effort at different depths.
- **Average Decision Time:** Measure how long the AI takes to choose a move.
- **Tactical Accuracy:** Test whether the AI recognizes immediate winning moves and blocks immediate opponent wins.

The planned evaluation includes at least 100 games per configuration, using fixed documented seeds and balanced starting-player assignments. Results will be presented through charts comparing performance across search depths.

## 🚀 Getting Started

### Prerequisites

- Python 3 installed.
- Git installed.
- Any additional dependencies required by the final implementation.

### Installation

Clone the repository:

```bash
git clone https://github.com/Faiza-usmani/Connect-Four-.git
```

Navigate to the project directory:

```bash
cd Connect-Four-
```

Install dependencies if a `requirements.txt` file is provided:

```bash
pip install -r requirements.txt
```

### Running the Game

Once the implementation is complete, run the project's main Python file:

```bash
python main.py
```

Replace `main.py` with the actual entry-point filename if it differs.

## 📁 Sample Project Structure

The planned code organization includes the following components:

```text
Connect-Four-/
├── main.py                 # Application entry point
├── board.py                # Board representation and game rules
├── game.py                 # Turn management and game flow
├── agent.py                # Base agent interface
├── random_agent.py         # Random-move baseline
├── minimax_agent.py        # Minimax, pruning, and evaluation
├── gui.py                  # Graphical user interface
├── tests/                  # Game logic and AI tests
├── results/                # Evaluation results and charts
├── requirements.txt        # Project dependencies
└── README.md               # Project documentation
```

*The structure above is a suggested organization and should be updated to match the actual repository files.*

## 👥 Team Members

| Name | Roll Number | Responsibilities |
|---|---|---|
| Faiza Usmani | 24K-2006 | AI algorithms, heuristic evaluation, testing, and performance analysis |
| Rabia Hakeem | 24K-2042 | Board logic, legal moves, win/draw detection, and integration testing |
| Wajiha Habibullah | 24K-2004 | GUI, game controls, documentation, charts, and integration support |

## 🔮 Future Improvements

Potential extensions include:
- Improved move ordering and search optimization.
- More advanced tactical evaluation.
- Additional AI difficulty levels.
- Enhanced interface design and animations.

Online multiplayer, user accounts, neural networks, and a perfect full-game solver are outside the current project scope.

## 🎓 Academic Information

**Course:** AL-2002 — Artificial Intelligence Laboratory  
**Institution:** FAST — National University of Computer and Emerging Sciences, Karachi Campus  
**Semester:** Fall 2026  
**Project:** Connect Four AI

