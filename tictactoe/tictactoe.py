import math
import random
import time
import Weight
X = "X"
O = "O"
EMPTY = '_'
WIN = 4
N = 5

def initial_state():
    return [[EMPTY for _ in range(N)] for _ in range(N)]

def player(board) -> str:
    count_X = sum(row.count(X) for row in board)
    count_O = sum(row.count(O) for row in board) 
    if count_X == count_O:
        return X
    else: # if count_X > count_O
        return O

def actions(board) -> set:
    possible = set()
    for i in range(N):
        for j in range(N):
            if board[i][j] == EMPTY:
                possible.add((i, j))
    return possible

def heuristic(board) -> int:
    score = 0
    # check row
    for row in board:
        line_str = ''.join(row)
        for k, v in Weight.patterns.items():
            if k in line_str:
                score += v
    # check column
    for col in range(N):
        line_str = ''.join(board[_][col] for _ in range(N))
        for k, v in Weight.patterns.items():
            if k in line_str:
                score += v
    # check main diagonal
    for i in range(N - WIN + 1):
        for j in range(N - WIN + 1):
            line_str = ''.join(board[i + k][j + k] for k in range(WIN))
            for k, v in Weight.patterns.items():
                if k in line_str:
                    score += v
    # check secondary diagonal:
    for i in range(N - WIN + 1):
        for j in range(WIN - 1, N):
            line_str = ''.join(board[i + k][j - k] for k in range(WIN))
            for k, v in Weight.patterns.items():
                if k in line_str:
                    score += v
    return score

def winner(board) -> str:
    maxWin = X*WIN
    minWin = O*WIN
    # check row
    for row in board:
        line_str = ''.join(row)
        if maxWin in line_str: return X 
        if minWin in line_str: return O
    # check column
    for col in range(N):
        line_str = ''.join(board[_][col] for _ in range(N))
        if maxWin in line_str: return X 
        if minWin in line_str: return O
    # check main diagonal
    for i in range(N - WIN + 1):
        for j in range(N - WIN + 1):
            line_str = ''.join(board[i + k][j + k] for k in range(WIN))
            if maxWin in line_str: return X 
            if minWin in line_str: return O
    # check secondary diagonal:
    for i in range(N - WIN + 1):
        for j in range(WIN - 1, N):
            line_str = ''.join(board[i + k][j - k] for k in range(WIN))
            if maxWin in line_str: return X 
            if minWin in line_str: return O
    # not win yet 
    return None

def terminal(board) -> bool:
    
    if winner(board) is not None: return True
    # check not win yet
    for i in range(N):
        for j in range(N):
            if board[i][j] == EMPTY:
                return False
    # tie
    return True

def utility(board) -> int:
    # If the game is not terminal yet, we have to heuristic the score of the game base on
    # patterns, like chance of winning for each player, who likely to win 
    # If the game is terminal, we return 1, -1, 0
    if terminal(board):
        notation = winner(board)
        if notation == X:
            return 100000
        elif notation == O:
            return -100000
        return 0
    # heuristic
    return heuristic(board)

def minimaxB(board, depth,isMaxPlayer, alpha, beta) -> tuple: # (val, i, j, cnt, has prunning)
    if board == initial_state():
        i, j = random.randint(0, N - 1), random.randint(0, N - 1)
        return (0, i, j, 1)
    if terminal(board) or depth == 0:
        return (utility(board), None, None, 1)
    if isMaxPlayer:
        maxEval = -math.inf
        best_i, best_j = None, None
        total_cnt = 0
        possible = actions(board)
        for action in possible:
            i, j = action
            board[i][j] = "X"
            value, tmp_i, tmp_j, node_cnt = minimaxB(board, depth - 1, False, alpha, beta)
            total_cnt += node_cnt + 1
            board[i][j] = EMPTY
            if value > maxEval:
                maxEval, best_i, best_j = value, i, j
            alpha = max(value, alpha)
            if beta <= alpha:
                break
        return (maxEval, best_i, best_j, total_cnt)
    if not isMaxPlayer:
        minEval = math.inf
        best_i, best_j = None, None
        total_cnt = 0
        possible = actions(board)
        for action in possible:
            i, j = action
            board[i][j] = "O"
            value, tmp_i, tmp_j, node_cnt = minimaxB(board, depth - 1, True, alpha, beta)
            total_cnt += node_cnt + 1
            board[i][j] = EMPTY
            if value < minEval:
                i, j = action
                minEval, best_i, best_j = value, i, j
            beta = min(value, beta)
            if beta <= alpha:
                break
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
