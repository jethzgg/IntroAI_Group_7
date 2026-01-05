import math
import random
import time

X = "X"
O = "O"
EMPTY = '_'
WIN_LENGTH = 4
N = 5
MAX_DEPTH = 4
lastX, lastY = None, None
ai_time = 0

patterns = {
    # X patterns (Maximizing) 
    # Sắp thắng (không chặn được)
    "_XXX_": 100000000,
    # Sắp thắng (có thể chặn 1 đầu)
    "XXX_": 1000000,
    "_XXX": 1000000,
    "XX_X": 100000,
    "X_XX": 100000,  
    # 2 quân liên tiếp
    "_XX_": 100000,
    "_X_X_": 5000, 
    "XX__": 10000,
    "__XX": 10000,
    "X__X": 500,   
    # 1 quân
    "_X___": 100,
    "__X__": 2,
    "_X___": 1,
    "___X_": 1,
    # O patterns (Minimizing)
    "_OOO_": -100000000,
    "OOO_": -1000000,
    "_OOO": -1000000,
    "OO_O": -100000,
    "O_OO": -100000,
    "_OO_": -100000,
    "_O_O_": -5000,
    "OO__": -10000,
    "__OO": -10000,
    "O__O": -500,  
    "_O_": -100,
    "__O__": -2,
    "_O___": -1,
    "___O_": -1
}

def initialState() -> list[list[str]]:
    return [[EMPTY for _ in range(N)] for _ in range(N)]

def getValidMove(board) -> list[tuple[int, int]]: 
    moves = list()
    for i in range(N):
        for j in range(N):
            if board[i][j] == EMPTY:   
               moves.append((i, j))
    return list(moves)

def whoseTurn(board) -> str:
    cntX = sum(1 for row in board for cell in row if cell == X)
    cntO = sum(1 for row in board for cell in row if cell == O)
    if cntX == cntO:
        return X
    return O
def winner(board, player) -> bool:
    # check row
    for x in range(N):
        for y in range(N - WIN_LENGTH + 1):
            if all(board[x][y + k] == player for k in range(WIN_LENGTH)):
                return True
    # check column
    for y in range(N):
        for x in range(N - WIN_LENGTH + 1):
            if all(board[x + k][y] == player for k in range(WIN_LENGTH)):
                return True
    # check main diagonal
    for x in range(N - WIN_LENGTH + 1):
        for y in range(N - WIN_LENGTH + 1):
            if all(board[x + k][y + k] == player for k in range(WIN_LENGTH)):
                return True
    # check secondarey diagonal
    for x in range(N - WIN_LENGTH + 1):
        for y in range(WIN_LENGTH - 1, N):
            if all(board[x + k][y - k] == player for k in range(WIN_LENGTH)):
                return True
    # no winner
    return False

def isTerminal(board) -> bool:
    # This function has to be fast since for every minimax call, it is called 
    if winner(board, X) or winner(board, O):
        return True
    for x in range(N):
        for y in range(N):
            if board[x][y] == EMPTY:
                return False
    return True

def heuristic(board) -> int:
    score  = 0
    for row in board:
        row_str = ''.join(row)
        for p, val in patterns.items():
            if p in row_str:
                score += val
    for col in range(N):
        col_str = ''.join(board[row][col] for row in range(N))
        for p, val in patterns.items():
            if p in col_str:
               score += val
    for i in range(N - WIN_LENGTH + 1): 
        for j in range(N - WIN_LENGTH + 1): 
            diag = ''.join(board[i + k][j + k] for k in range(WIN_LENGTH))
            for p, val in patterns.items():
                if p in diag:
                    score += val
    for i in range(N - WIN_LENGTH + 1):
        for j in range(WIN_LENGTH - 1, N):
            diag = ''.join(board[i + k][j - k] for k in range(WIN_LENGTH))
            for p, val in patterns.items():
                if p in diag:
                    score += val
    return score

def minimax(board, depth, alpha, beta, maxPlayer) -> int:
    # end of recursion
    if isTerminal(board):
        if winner(board, X):
            return 100000000
        if winner(board, O):
            return -100000000
        return 0
    if depth == 0:
        return heuristic(board)
    # available moves
    moves = getValidMove(board)
    # recursion
    if maxPlayer:
        maxValue = -math.inf
        for x, y in moves:
            board[x][y] = X
            value = minimax(board, depth - 1, alpha, beta, False)
            board[x][y] = EMPTY
            maxValue = max(maxValue, value)
            alpha = max(alpha, value)
            if beta <= alpha:
                break
        return maxValue
    if not maxPlayer:
        minValue = math.inf
        for x, y in moves:
            board[x][y] = O
            value = minimax(board, depth - 1, alpha, beta, True)
            board[x][y] = EMPTY
            minValue = min(minValue, value)
            beta = min(beta, value)
            if beta <= alpha:
                break
        return minValue
    
def bestMove(board) -> tuple[int, int]:
    global ai_time
    player = whoseTurn(board)
    moves = getValidMove(board)
    best_x, best_y = None, None
    start_time = time.perf_counter()
    step = sum(1 for row in board for cell in row if cell != EMPTY) 
    if step == 0:
        end_time = time.perf_counter()
        ai_time += end_time - start_time
        return (N // 2, N // 2)
    elif step == 1:
        if board[2][2] == EMPTY:
            return (N // 2, N // 2)
        choice = [1, 3]
        x = choice[random.randint(0, 1)]
        y = choice[random.randint(0, 1)]
        end_time = time.perf_counter()
        ai_time += end_time - start_time
        return (x, y)
    # In here, the best move is the move that has the best minimax value for AI player
    # If AI is X, we want to maximize the minimax value
    # If AI is O, we want to minimize the minimax value
    if player == X:
        maxValue = -math.inf
        for x, y in moves:
            board[x][y] = X
            value = minimax(board, MAX_DEPTH, -math.inf, math.inf, False)
            board[x][y] = EMPTY
            if value > maxValue:
                maxValue = value
                best_x, best_y = x, y
    if player == O:
        minValue = math.inf
        for x, y in moves:
            board[x][y] = O
            value = minimax(board, MAX_DEPTH, -math.inf, math.inf, True)
            board[x][y] = EMPTY
            if value < minValue:
                minValue = value
                best_x, best_y = x, y
    end_time = time.perf_counter()
    ai_time += end_time - start_time
    return (best_x, best_y)