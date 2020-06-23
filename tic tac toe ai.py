import copy
import numpy as np
board = [[' '] * 3 for x in range(3)]


def whose_turn(position):
    turn_helper = 0
    for i in range(3):
        for j in range(3):
            if position[i][j] != ' ':
                turn_helper += 1
    return 'X' if turn_helper % 2 == 0 else 'O'


def is_full(position):
    for i in range(3):
        for j in range(3):
            if position[i][j] == ' ':
                return False
    return True


def get_plays(position):
    plays = []
    symbol = 'X' if whose_turn(position) == 'X' else 'O'
    for i in range(3):
        for j in range(3):
            if position[i][j] == ' ':
                plays.append(copy.deepcopy(position))
                plays[-1][i][j] = symbol
    return plays


def check_for_win(position):
    invert_symbol = 'O' if whose_turn(position) == 'X' else 'X'
    for i in range(3):
        if position[i][0] == position[i][1] == position[i][2] != ' ':
            return invert_symbol
        if position[0][i] == position[1][i] == position[2][i] != ' ':
            return invert_symbol
    if position[0][0] == position[1][1] == position[2][2] != ' ':
        return invert_symbol
    if position[0][2] == position[1][1] == position[2][0] != ' ':
        return invert_symbol
    return 'Draw'


def solve(position):
    if check_for_win(position) != 'Draw':
        return check_for_win(position)
    if is_full(position):
        return 'Draw'
    plays = get_plays(position)
    check_play = np.array([solve(plays[i]) for i in range(len(plays))])
    x_wins = np.where(check_play == 'X')
    o_wins = np.where(check_play == 'O')
    draw = np.where(check_play == 'Draw')

    if whose_turn(position) == 'X':
        if 'X' in check_play:
            return 'X'
        elif 'Draw' in check_play:
            return 'Draw'
        else:
            return 'O'
    else:
        if 'O' in check_play:
            return 'O'
        elif 'Draw' in check_play:
            return 'Draw'
        else:
            return 'X'


pos_1 = [[' ', ' ', ' '],
         ['X', 'O', ' '],
         [' ', ' ', ' ']]
print(solve(pos_1))
