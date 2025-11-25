"""
Tic Tac Toe Player
"""


import math
import copy
import random


X = "X"
O = "O"
EMPTY = None


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


def check(user,board):
    for row in board:
        count_user = row.count(user)
        if count_user >= 4:
            for i in range(1, 4):
                if row[i] != user:
                    return False
            return True
    a = 0
    b = 1
    while (0 <= a and a < 5 and 0 <= b and b < 5):
        if board[i][j] != user: return False
        a += 1
        b += 1
    a = 1
    b = 0
    while (0 <= a and a < 5 and 0 <= b and b < 5):
        if board[i][j] != user: return False
        a += 1
        b += 1
    a = 3
    b = 0
    while (0 <= a and a < 5 and 0 <= b and b < 5):
        if board[i][j] != user: return False
        a -= 1
        b += 1
    a = 4
    b = 1
    while (0 <= a and a < 5 and 0 <= b and b < 5):
        if board[i][j] != user: return False
        a -= 1
        b += 1
    temp = []
    i = 0
    j = 0
    while (i < 5 and j < 5):
        temp.append(board[i][j])
        i += 1
        j += 1
    if temp.count(user) >= 4:
        for i in range (1, 4):
            if temp[i] != user:
                return False
    i = 4
    j = 0
    while (i >= 0 and j < 5):
        temp.append(board[i][j])
        i -= 1
        j += 1
    if temp.count(user) >= 4:
        for i in range (1, 4):
            if temp[i] != user:
                return False
    return True

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


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    if winner(board) == O:
        return -1
    return 0


def maxValue(board):
    global actions1
    if terminal(board):
        return utility(board)
    v_max = -1
    for action in actions(board):
        v = minValue(result(board, action))
        if v_max == v:
            actions1.append(v)
        elif v_max < v:
            actions1 = [action]
            v_max = v
    return v


def minValue(board):
    global actions2
    if terminal(board):
        return utility(board)
    v_min = 1
    for action in actions(board):
        v = maxValue(result(board, action))
        if v_min == v:
            actions2.append(v)
        elif v_min > v:
            actions2 = [action]
            v_min = v
    return v


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
            actions1 = []
            value = maxValue(board)
            i = random.randint(0,len(actions1)-1)
            return actions1[i]
        if turn == O:
            actions2 = []
            value = minValue(board)
            i = random.randint(0,len(actions2)-1)
            return actions2[i]