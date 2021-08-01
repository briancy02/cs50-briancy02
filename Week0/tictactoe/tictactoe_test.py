import pytest
import tictactoe
X = "X"
O = "O"
EMPTY = None

def test_player():
    x_first_board = [[X, O, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]
    o_first_board = [[O, X, X],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]        
    assert tictactoe.player(x_first_board) 
    assert tictactoe.player(o_first_board)  
    
def test_actions():
    board = [[X, O, EMPTY],
            [EMPTY, X, O],
            [X, O, X]]
    print(tictactoe.actions(board)[0])        
    assert tictactoe.actions(board) == [(0, 2), (1, 0)]  


ver_win_1 =  [[X, O, O],
            [X, EMPTY, O],
            [X, O, X]]
ver_win_2 = [[X, O, X],
            [EMPTY, O, O],
            [X, O, X]]
ver_win_3 = [[X, O, X],
            [O, EMPTY, X],
            [O, O, X]]
hor_win_1 = [[X, EMPTY, O],
            [O, EMPTY, O],
            [X, X, X]]
hor_win_2 = [[X, EMPTY, X],
            [O, O, O],
            [X, O, X]]
hor_win_3 = [[X, X, X],
            [EMPTY, O, O],
            [X, O, EMPTY]]
diag_win_1 = [[X, O, X],
            [EMPTY, X, O],
            [X, O, EMPTY]]
diag_win_2 = [[X, O, EMPTY],
            [EMPTY, X, O],
            [X, O, X]]
full_board = [[X, O, X],
            [O, O, X],
            [X, X, O]]           


def test_utility():
    assert tictactoe.utility(ver_win_1) == 1
    assert tictactoe.utility(ver_win_2) == -1
    assert tictactoe.utility(ver_win_3) == 1
    assert tictactoe.utility(hor_win_1) == 1
    assert tictactoe.utility(hor_win_2) == -1
    assert tictactoe.utility(hor_win_3) == 1
    assert tictactoe.utility(diag_win_2) == 1
    assert tictactoe.utility(diag_win_1) == 1
    
def test_terminal():
    assert tictactoe.terminal(ver_win_1)
    assert tictactoe.terminal(full_board)
    
            
