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
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


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
    for i in range(3):
        for j in range (3):
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
    for i in range(3):
        if board[i] == [user,user,user]:
            return True
    for j in range(3):
        if board[0][j] == board[1][j] and board[1][j] == board[2][j] and board[2][j] == user:
            return True
    if board[0][0] == board[2][2] and board[2][2] == board[1][1] and board[1][1] == user:
        return True        
    if board[0][2] == board[2][0] and board[2][0] == board[1][1] and board[1][1] == user:
        return True
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


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    if winner(board) == O:
        return -1
    return 0


actions1 = []
def maxv(board):
    global actions1
    if terminal(board):
        return utility(board)
    va = -1
    v = va
    for action in actions(board):
        v = minv(result(board,action))
        if v == 1:
            actions1 = [action]
            return v
        if v > va:
            va = v
            actions1 = [action]
        elif v == va:
            actions1.append(action)
        else:
            pass
    return v


actions2 = []
def minv(board):
    global actions2
    if terminal(board):
        return utility(board)
    va = 1
    v = va
    for action in actions(board):
        v = maxv(result(board,action))
        if v == -1:
            actions2 = [action]
            return v
        if v < va:
            va = v
            actions2 = [action]
        elif v == va:
            actions2.append(action)
        else:
            pass
    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if board == initial_state():
        i = random.randint(0,2)
        j = random.randint(0,2)
        return (i,j)
    if terminal(board) == False:
        turn = player(board)
        if turn == X:
            value = maxv(board)
            action = actions1
            i = random.randint(0,len(action)-1)
            return action[i]
        if turn == O:
            value = minv(board)
            action = actions2
            i = random.randint(0,len(action)-1)
            return action[i]