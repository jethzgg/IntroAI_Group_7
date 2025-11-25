"""
Tic Tac Toe Player
"""


import math
import copy
import random


X = "X"
O = "O"
EMPTY = None
MAX_DEPTH = 3

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # Count the number of 'X's and 'O's on the board to determine the player turn
    count_X = sum(row.count(X) for row in board)
    count_O = sum(row.count(O) for row in board)
    
    # Determine whose turn it is based on the counts
    if count_X == count_O:
        return 'X'  # It's X's turn
    else:
        return 'O'  # It's O's turn


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible = set()
    for i in range(5):
        for j in range (5):
            if board[i][j] == EMPTY:
                possible.add((i,j))
    return possible


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    possible = actions(board)
    turn = player(board)
    new_board = copy.deepcopy(board)
    i,j = action
    if (i,j) not in possible:
        raise Exception("NOT VALID MOVE")
    else:
        new_board[i][j] = turn
    return new_board


def check_line(line, user):
    count = 0
    for cell in line:
        if cell == user:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    return False

def check(user, board):
    """
    Return True if user is the winner
    """
    for row in board:
        if check_line(row, user): return True
    
    for col in range(5):
        column = [board[row][col] for row in range(5)]
        if check_line(column, user): return True
        
    diagonals = []
    
    diagonals.append([board[i][i] for i in range(5)])
    diagonals.append([board[i][i+1] for i in range(4)])
    diagonals.append([board[i+1][i] for i in range(4)])
    
    diagonals.append([board[i][4-i] for i in range(5)])
    diagonals.append([board[i][3-i] for i in range(4)])
    diagonals.append([board[i+1][4-i] for i in range(4)])
    
    for diag in diagonals:
        if check_line(diag, user): return True
            
    return False


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if check(X,board) == True and check(O,board) == True: raise Exception("INVALID BOARD STATE")
    if check(X,board):
        return X
    elif check(O,board):
        return O
    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Check for a win
    if check(X,board) or check(O,board):
        return True
    
    for row in board:
        for cell in row:
            if cell == EMPTY:
                return False
    return True

def evaluate_line(line):
    return 0

def evaluate(board):
    score = 0
    for row in board:
        pass
    return 0

def maxValue(board, max_value, min_value, depth):
    if terminal(board) or depth == MAX_DEPTH:
        return evaluate(board), None
    
    best_move = None
    val = -math.inf

    for action in actions(board):
        v, _ = minValue(result(board, action), max_value, min_value, depth + 1)
        if v > val:
            best_move = action
            val = v
        max_value = max(max_value, val)
        if max_value >= min_value:
            break
    return max_value, best_move


def minValue(board, max_value, min_value, depth):
    if terminal(board) or depth == MAX_DEPTH:
        return evaluate(board), None
    
    best_move = None
    val = math.inf
    
    for action in actions(board):
        v, _ = maxValue(result(board, action), max_value, min_value, depth + 1)
        if v < val:
            best_move = action
            val = v
        min_value = min(min_value, val)
        if (min_value <= max_value):
            break
    return min_value, best_move

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if board == initial_state():
        i = random.randint(0,4)
        j = random.randint(0,4)
        return (i,j)
    if terminal(board) == False:
        turn = player(board)
        if turn == X:
            _, action = maxValue(board, 0)
            
        if turn == O:
            _, action = minValue(board, 0)

        return action 