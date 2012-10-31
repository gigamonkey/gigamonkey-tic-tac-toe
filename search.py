#!/usr/bin/env python3

from itertools import permutations
import random

# Board representation: 9-tuple of Xs, Os, and Nones.

rows  = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
cols  = [[0, 3, 6], [1, 4, 7], [2, 5, 8]]
diags = [[0, 4, 8], [6, 4, 2]]
lines = rows + cols + diags

board_fmt = "---+---+---\n".join([" {} | {} | {}\n"] * 3)

def show(p):
    print(board_fmt.format(*[x or i for i, x in enumerate(p)]))

def game_state(position):
    threes = list({ three_in_a_row(position, line) for line in lines } - { None })
    if len(threes) == 1 and to_play(position) != threes[0]:
        return threes[0]
    elif len(threes) == 0:
        return 'draw' if position.count(None) == 0 else 'in_progress'
    else:
        return False

def three_in_a_row(position, line):
    marks = [ position[i] for i in line if position[i] ]
    return marks[0] if len(marks) == 3 and len(set(marks)) == 1 else None

def to_play(position):
    return 'XO'[position.count('X') - position.count('O')]

def possible_moves(position):
    mark = to_play(position)
    for i in filter(lambda x: position[x] == None, range(9)):
        new = position[:i] + (mark,) + position[i+1:]
        if game_state(new): yield i, new

def search(position):
    state = game_state(position)
    if   state == 'X': return (1, None)
    elif state == 'O': return (-1, None)
    elif state == 'draw': return (0, None)
    elif state == 'in_progress':
        player     = to_play(position)
        best_score = None
        best_move  = None

        def better(s):
            return s > best_score if player == 'X' else s < best_score

        for m, p in possible_moves(position):
            score, _ = search(p)
            if best_score is None or better(score):
                best_score = score
                best_move = m
        return (best_score, best_move)

    else: raise Exception("Can't score illegal position {}".format(position))


def play(human, position):
    while game_state(position) == 'in_progress':
        show(position)
        if to_play(position) == human:
            move = int(input("Move: "))
        else:
            _, move = search(position)
        position = position[:move] + (to_play(position),) + position[move+1:]
    show_result(position, human)

def show_result(position, human):
    show(position)
    state = game_state(position)
    if state == human:
        print("You win!")
    elif state == 'draw':
        print("Good fight. Tie.")
    else:
        print("I win. How about a nice game of global thermonuclear war?")

if __name__ == '__main__':
    import sys
    play(sys.argv[1], (None,) * 9)
