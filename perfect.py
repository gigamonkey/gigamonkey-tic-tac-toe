#!/usr/bin/env python3

from itertools import permutations
import random

# Represent a tic-tac-toe board as a list of nine elements.

# 0 | 1 | 2
# ---------
# 3 | 4 | 5
# ---------
# 6 | 7 | 8

verbose = False

rows  = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
cols  = [[0, 3, 6], [1, 4, 7], [2, 5, 8]]
diags = [[0, 4, 8], [6, 4, 2]]
lines = rows + cols + diags

def to_string(p):
    return ''.join([(x if x is not None else '_') for x in p])

def show(p):
    print('''
 {} | {} | {}
---+---+---
 {} | {} | {}
---+---+---
 {} | {} | {}

'''.format(*[x if x is not None else i for i, x in enumerate(p)]))

def three_in_a_row(position, line):
    "Return 'X' or 'O' if line is three in a row of that mark in position, None otherwise"
    marks = [ position[i] for i in line if position[i] is not None ]
    return marks[0] if len(marks) == 3 and len(set(marks)) == 1 else None

def is_legal(position):
    threes = [x for x in (three_in_a_row(position, line) for line in lines) if x is not None]
    if len(set(threes)) == 1 and to_play(position) != threes[0]:
        return threes[0]
    elif len(threes) == 0:
        if moves(position) == 9:
            return 'draw'
        else:
            return 'in_progress'
    else:
        return False

def moves(position):
    return 9 - position.count(None)

def to_play(position):
    return 'XO'[position.count('X') - position.count('O')]

def legal_positions(n):
    "Generate all legal positions of N moves."
    def walk(n, position, seen):
        mark = 'XO'[(9 - n) % 2]
        if n > 0:
            for i in range(9):
                if position[i] is None:
                    p = position[:]
                    p[i] = mark
                    if tuple(p) not in seen:
                        seen.add(tuple(p))
                        for x in walk(n - 1, p, seen): yield x
        else:
            if is_legal(position): yield position

    for x in walk(n, [None] * 9, set()): yield x

def other_legal_positions(n):
    marks = list('XOXOXOXOX'[:n]) + ([None] * (9 - n))

    return set(p for p in set(p for p in permutations(marks, 9)) if is_legal(p))

def score(position, db):
    state = is_legal(position)

    if verbose: print('Scoring {} {} to move ({})'.format(to_string(position), to_play(position), state))

    if state == 'X':
        return { 'score': 1, 'moves': None }
    elif state == 'O':
        return { 'score': -1, 'moves': None }
    elif state == 'draw':
        return { 'score': 0, 'moves': None }
    elif state == 'in_progress':
        return find_best_score(position, db)
    else:
        raise Exception("Can't score illegal position {}".format(position))

def find_best_score(position, db):
    player     = to_play(position)
    best_score = None
    moves      = None

    def better(score):
        if player == 'X':
            return score > best_score
        else:
            return score < best_score

    for move, p in possible_moves(position):
        score = db[p]['score']
        if verbose: print('  Move {} to {} => score: {}'.format(move, to_string(p), score))
        if best_score is None or better(score):
            best_score = score
            moves = [ move ]
        elif score == best_score:
            moves.append(move)


    return { 'score': best_score, 'moves': moves }

def possible_moves(position):
    mark = to_play(position)
    for i in range(9):
        if position[i] == None:
            new = position[:]
            new[i] = mark
            if is_legal(new):
                yield i, to_string(new)


def play(db, position=None):
    if position is None:
        position = [None]  * 9
    else:
        position = [ x if x != '_' else None for x in position ]

    while is_legal(position) == 'in_progress':
        show(position)
        print(db[to_string(position)])
        print('')
        if to_play(position) == 'X':
            move = int(input("Move: "))
        else:
            move = pick_move(position, db)

        position[move] = to_play(position)

    show(position)
    print(is_legal(position))


def pick_move(position, db):
    return random.choice(db[to_string(position)]['moves'])

def load_db():
    db = {}
    for n in range(9, -1, -1):
        for p in legal_positions(n):
            db[to_string(p)] = score(p, db)
    return db

if __name__ == '__main__':

    for i in range(10):
        print('{} => {}'.format(i, (other_legal_positions(9) == set(tuple(p) for p in legal_positions(9)))))

    import sys

    play(load_db(), sys.argv[1] if len(sys.argv) > 1 else None)
