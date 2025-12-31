import math
import time
import random

X = "X"
O = "O"
EMPTY = '_'
WIN_LENGTH = 4
N = 5
MAX_DEPTH = 4
lastX, lastY = N // 2, N // 2

patterns = {
    "XXXX": 1000000,
    "_XXX_": 100000,
    "XXX_": 10000,
    "_XXX": 10000,
    "XX_X": 10000,
    "X_XX": 10000,
    "_XX_": 1000,
    "XX__": 100,
    "__XX": 100,
    "_X_X_": 500,
    "X__X": 50,
    "_X_": 10,
    "__X__": 2,
    "_X___": 1,
    "___X_": 1,
    
    "OOOO": -1000000,
    "_OOO_": -100000,
    "OOO_": -10000,
    "_OOO": -10000,
    "OO_O": -10000,
    "O_OO": -10000,
    "_OO_": -1000,
    "OO__": -100,
    "__OO": -100,
    "_O_O_": -500,
    "O__O": -50,
    "_O_": -10,
    "__O__": -2,
    "_O___": -1,
    "___O_": -1,
}

def initialState() -> list:
    return [[EMPTY for _ in range(N)] for _ in range(N)]

def getValidMove(board, radius) -> list:
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
    player = whoseTurn(board)
    score  = 0
    for row in board:
        row_str = ''.join(row)
        for p, val in patterns.items():
            if p in row_str:
                if (player == X):
                    score = max(score, val)
                else:
                    score = min(score, val)
    # check columns
    for col in range(N):
        col_str = ''.join(board[row][col] for row in range(N))
        for p, val in patterns.items():
            if p in col_str:
                if (player == X):
                    score = max(score, val)
                else:
                    score = min(score, val)

    for i in range(N - WIN_LENGTH + 1): # for i in range(2)
        for j in range(N - WIN_LENGTH + 1): # for j in range(2)
            diag = ''.join(board[i + k][j + k] for k in range(WIN_LENGTH))
            for p, val in patterns.items():
                if p in diag:
                    if (player == X):
                        score = max(score, val)
                    else:
                        score = min(score, val)

    for i in range(N - WIN_LENGTH + 1):
        for j in range(WIN_LENGTH - 1, N):
            diag = ''.join(board[i + k][j - k] for k in range(WIN_LENGTH))
            for p, val in patterns.items():
                if p in diag:
                    if (player == X):
                        score = max(score, val)
                    else:
                        score = min(score, val)
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