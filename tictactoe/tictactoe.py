"""
Tic Tac Toe Player
"""

import math
import util

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

# COMPLETE
def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = 0;
    o_count = 0;
    for row in board:
        for elem in row:
            if elem == X:
                x_count += 1
            elif elem == O:    
                o_count += 1
    if x_count > o_count:
        return O
    return X    


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = list()
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == EMPTY:
                actions.append((i,j))
    return actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board[action[0]][action[1]] = player(board)

    return board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(len(board)):
        needed = board[i][0]
        for j in range(1, len(board[0])):
            if needed != board[i][j]:
                break
            elif j == 2:
                # return winner
                return board[i][j]
                
    for i in range(len(board)):
        needed = board[0][i]
        for j in range(1, len(board[0])):
            if needed != board[j][i]:
                break
            elif j == 2:
                # return winner
                return board[j][i]  
    
    for i in range(1, len(board)):
        needed = board[0][0]
        if needed != board[i][i]:
            break
        elif i ==2:
            return board[i][i]
    for i in range(1, len(board)):
        needed = board[len(board) - 1][0]
        if needed != board[len(board) - 1 - i][i]:
            break
        elif i == 2:
            return board[len(board) - 1 - i][i]        
            
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
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
    won = winner(board)
    if won == X:
        return 1
    elif won == O:
        return -1
    else:
        return 0



def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    actions = actions(board)
    optimal_action = None
    player = player(board)
    if player == 'X':
        max_value = min;
        for action in actions:
            new_max = max_value(result(board, action))
            if max_value < new_max:
                optimal_action = action
                max_value = new_max
    elif player == 'O':
        min_value = max;
        for action in actions:
            new_min = min_value(result(board, action))
            if min_value > new_min:
                optimal_action = action
                min_value = new_min   
    return optimal_action            
