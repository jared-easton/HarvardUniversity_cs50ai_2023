"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

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
    # raise NotImplementedError
    Xnum = 0
    Onum = 0

    for row in board:
        Xnum += row.count(X)
        Onum += row.count(O)

    if Xnum <= Onum:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # raise NotImplementedError
    options = set()

    for row_index, row in enumerate(board):
        for column_index, item in enumerate(row):
            if item == None:
                options.add((row_index, column_index))

    return options


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    ## raise NotImplementedError
    player_action = player(board)

    new_game = deepcopy(board)
    i, j = action

    if board[i][j] != None:
        raise Exception
    else:
        new_game[i][j] = player_action

    return new_game


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    ## raise NotImplementedError
    for player in (X, O):
        # vertical
        for row in board:
            if row == [player] * 3:
                return player
            
        # horizontal
        for w in range(3):
            column = [board[l][w] for l in range(3)]
            if column == [player] * 3:
                return player
            
        # diagonal
        if [board[w][w] for w in range(0, 3)] == [player] * 3:
            return player
        
        elif [board[w][~w] for w in range(0, 3)] == [player] * 3:
              return player
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    ## raise NotImplementedError
    # a player wins
    if winner(board) != None:
        return True
    
    # more moves in game
    for row in board:
        if EMPTY in row:
            return False
        
    # no more moves in game
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    ## raise NotImplementedError

    win_game = winner(board)

    if win_game == X:
        return 1
    elif win_game == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    ## raise NotImplementedError
    def max_value(board):
        optimal_move = ()
        if terminal(board):
            return utility(board), optimal_move
        else: 
            f = -5
            for action in actions(board):
                minval = min_value(result(board, action))[0]
                if minval > f:
                    f = minval
                    optimal_move = action
                return f, optimal_move
            
    def min_value(board):
        optimal_move = ()
        if terminal(board):
            return utility(board), optimal_move
        else:
            f = 5
            for action in actions(board):
                maxval = max_value(result(board, action))[0]
                if maxval < f:
                    f = maxval
                    optimal_move = action
            return f, optimal_move
        
    live_player = player(board)

    if terminal(board):
        return None
    
    if live_player == X:
        return max_value(board)[1]
    
    else: return min_value(board)[1]
