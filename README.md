# Tic-tac-toe - Group 7

** IT3160E Introduction to Artificial Intelligence - Hanoi University of Science and Technology **

## Description

This repository contains the source code of a Tic-tac-toe game with an AI opponent. The AI uses the Minimax algorithm to make optimal moves.
Therefore, it also contains a web API built with FastAPI to interact with the game and frontend clients using ReactJS and ViteJS.

## Dependencies

### Backend (Python)
- Python 3.10+
- fastapi
- uvicorn
- pydantic
- pygame-ce

### Frontend (JavaScript)
- Node.js 20+
- React 19
- Vite 7
- Tailwind CSS 4
- React Router 7
- React Icons

## Installation

### 1. Clone the repository:

```bash
git clone https://github.com/jethzgg/IntroAI_Group_7.git
cd IntroAI_Group_7
```

### 2. Set up the backend:

```bash
cd tictactoe
python -m venv .venv
source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
pip install -r requirements.txt
uvicorn web_api:app --reload
```

Backend will be running at `http://localhost:8000`

### 3. Set up the frontend:
#### Open another terminal window and run:

```bash
git worktree add ../IntroAI_frontend frontend
cd ../IntroAI_frontend
npm install
npm run dev
```

Frontend will be running at `http://localhost:5173`

### 4. Using Desktop Application version:

```bash
cd ../IntroAI_Group_7/tictactoe
source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
pip install -r requirements.txt
python runner.py
```

## 📁 Project Structure

```
IntroAI_Group_7/
├── tictactoe/
│   ├── tictactoe.py      # Logic game and AI (Minimax, Alpha-Beta)
│   ├── web_api.py        # FastAPI backend server
│   ├── runner.py         # Pygame desktop version
│   └── requirements.txt  # Python dependencies
│
└── (branch:  frontend)
    ├── src/
    │   ├── api/          # API calls to backend
    │   ├── components/   # React components
    │   └── pages/        # App pages
    └── package.json      # Node.js dependencies
```

## How to Play

- Open the frontend in your web browser at `http://localhost:5173`
- Start a new game and choose your symbol (X or O)
- Make your moves by clicking on the grid
- The AI will respond with its move
- The game ends when there is a winner or a draw

## Reproduce Key Results Shown in the Report

### 1. Minimax algorithm choosing the best move on a random board:

```bash
cd tictactoe
python -c "
    import tictactoe as ttt

    # Create a sample board
    board = board = [
        ['X', 'O', '_', '_', '_'],
        ['_', 'X', '_', '_', '_'],
        ['_', '_', 'O', '_', '_'],
        ['_', 'X', '_', '_', '_'],
        ['_', '_', '_', '_', '_']
    ]

    # Get the best move using Minimax
    best_move = ttt.bestMove(board)
    print(f'Best move for empty board: {best_move}')
"
```

### 2. Heuristic evaluation of a non-terminal board state:

```bash
cd tictactoe
python -c "
    import tictactoe as ttt
    board = [
        ['X', 'O', '_', '_', '_'],
        ['_', 'X', '_', '_', '_'],
        ['_', '_', 'O', '_', '_'],
        ['_', 'X', '_', '_', '_'],
        ['_', '_', '_', '_', '_']
    ]
    score = ttt.heuristic(board)
    print(f'Heuristic score: {score}')
"
```

### 3. AI performance:

```bash
cd tictactoe
python -c "
    import tictactoe as ttt
    import time
    board = [
        ['X', 'O', '_', '_', '_'],
        ['_', 'X', '_', '_', '_'],
        ['_', '_', 'O', '_', '_'],
        ['_', 'X', '_', '_', '_'],
        ['_', '_', '_', '_', '_']
    ]
    start_time = time.time()
    move = ttt.bestMove(board)
    end_time = time.time()
    print(f'Time to calculate best move: {(end_time - start_time) * 1000:.2f}ms')
"
```
