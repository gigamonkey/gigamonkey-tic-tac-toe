#!/usr/bin/env python3

from itertools import permutations

# Represent a tic-tac-toe board as a list of nine elements.

# 0 | 1 | 2
# ---------
# 3 | 4 | 5
# ---------
# 6 | 7 | 8

all_final_positions = list(permutations('XXXXXOOOO', 9))

rows  = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
cols  = [[0, 3, 6], [1, 4, 7], [2, 5, 8]]
diags = [[0, 4, 8], [6, 4, 5]]
lines = rows + cols + diags

def winners(position):
    return [ x for x in (three_in_a_row(position, line) for line in lines) if x is not None ]

def is_illegal(position):
    return len(winners(position)) > 1

def is_tie(position):
    return len(winners(position)) == 0

def the_winner(position):
    return winners(position)[0]

def whose_move(position):
    diff = 0
    for c in position:
        if c == 'X': diff += 1
        elif c == 'O': diff -= 1
    assert 0 <= diff <= 1, 'Illegal position: {}; diff: {}'.format(position, diff)
    return 'XO'[diff]

def pieces(position, line):
    return [ position[i] for i in line if position[i] is not None ]

def three_in_a_row(position, line):
    p = pieces(position, line)
    return p[0] if len(p) == 3 and len(set(p)) == 1 else None

def strip(board):
    return ''.join([ c for c in board if c in 'XO ' ])


# For all final positions discard illegal positions (multiple
# winners). Then for each position record the score (+1 if X won, -1
# if O won, and 0 if a draw). Then work backwards undoing each of the
# possible moves that could have gotten us to that position.

# If we know that position N wins for X than at any of the positions
# N-1, with X to play, X can win by playing to position N. So those
# positions are still +1. Then back up each of O's moves. In all of
# those positions, we know O can't play to any of the N-1 positions
# because they are +1. But if we've already figured out








if __name__ == '__main__':

    tie = '''
X | O | X
X | O | X
O | X | O'''


    print(winners('XXXOOOXXX'))
    print(winners('XXOXOOXOX'))
    print(winners(strip(tie)))
    print(whose_move('         '))
    print(whose_move('     X   '))
