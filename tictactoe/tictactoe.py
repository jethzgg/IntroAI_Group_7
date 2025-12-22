import math
import time
import random

X = "X"
O = "O"
EMPTY = '_'
WIN_LENGTH = 4
N = 5
MAX_DEPTH = 5
lastX, lastY = N // 2, N // 2

patterns = {
    "XXXX": 100000,
    "_XXX_": 50000,
    "XXX_": 10000,
    "_XXX": 10000,
    "_XX_": 4000,
    "XX__": 800,
    "__XX": 800,
    "_X_": 20,
    "__X__": 10,
    "_X___": 3,
    "___X_": 3,
    "OOOO": -100000,
    "_OOO_": -50000,
    "OOO_": -10000,
    "_OOO": -10000,
    "_OO_": -4000,
    "OO__": -800,
    "__OO": -800,
    "_O_": -20,
    "__O__": -10,
    "_O___": -3,
    "___O_": -3,
}

def initialState() -> list:
    return [[EMPTY for _ in range(N)] for _ in range(N)]

def getValidMove(board, radius) -> list: # most commonly, radius is 
    has_move = False
    moves = set()
    for i in range(N):
        for j in range(N):
            if board[i][j] != EMPTY:
                for dx in range(-radius, radius + 1):
                    for dy in range(-radius, radius + 1):
                        new_x, new_y = i + dx, j + dy
                        if 0 <= new_x < N and 0 <= new_y < N and board[new_x][new_y] == EMPTY:
                            has_move = True
                            moves.add((new_x, new_y))
    if not has_move:
        return [(N // 2, N // 2)]
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

def heuristic(board):
    score  = 0
    for row in board:
        row_str = ''.join(row)
        for p, val in patterns.items():
            if p in row_str:
                score += val
    # Cột
    for col in range(N):
        col_str = ''.join(board[row][col] for row in range(N))
        for p, val in patterns.items():
            if p in col_str:
               score += val

    for i in range(N - WIN_LENGTH + 1): # for i in range(2)
        for j in range(N - WIN_LENGTH + 1): # for j in range(2)
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
            return 1000000
        if winner(board, O):
            return -1000000
        return 0
    if depth == 0:
        return heuristic(board)
    # available moves
    moves = getValidMove(board, radius = 1)
    # sort base on manhattan
    moves.sort(key=lambda m: abs(m[0] - lastX) + abs(m[1] - lastY))
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
    
def bestMove(board) -> (tuple):
    player = whoseTurn(board)
    moves = getValidMove(board, radius = 1)
    best_x, best_y = None, None
    step = sum(1 for row in board for cell in row if cell != EMPTY) 
    if step == 0:
        return (N // 2, N // 2)
    elif step == 1:
        lowerX = lastX - 1 if lastX // 2 - 1 >= 0 else 0
        upperX = lastX + 1 if lastX // 2 + 1 < N else N
        lowerY = lastY - 1 if lastY // 2 - 1 >= 0 else 0
        upperY = lastY + 1 if lastY // 2 + 1 < N else N
        x, y = random.randint(lowerX, upperX), random.randint(lowerY, upperY)
        return (x, y)
    # In here, the best move is the move that has the highest value
    # The value of a move is the minValue for minPlayer if maxPlayer are considered to move
    # Otherwise, the value of a move is the maxValue for maxPlayer if the minPlayer are
    # considered to move
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
    return (best_x, best_y)
        return (minEval, best_i, best_j, total_cnt)

def minimax(board) -> tuple: # tuple of (best_i, best_j, count_node, time_run)
    turn = player(board)
    global Step
    Step = sum(1 for row in board for cell in row if cell is not EMPTY)
    depth = 5
    start = time.perf_counter()
    tmp_val, best_i, best_j, cnt = minimaxB(board, depth,  turn == X, -math.inf, math.inf)
    end = time.perf_counter()
    #print(f"da duyet {cnt} node trong {end - start:.4f} giay voi {Step} buoc")
    return (best_i, best_j)
