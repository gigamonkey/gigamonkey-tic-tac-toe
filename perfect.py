#!/usr/bin/env python3

from itertools import permutations
import random

rows  = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
cols  = [[0, 3, 6], [1, 4, 7], [2, 5, 8]]
diags = [[0, 4, 8], [6, 4, 2]]
lines = rows + cols + diags

board_fmt = "---+---+---\n".join([" {} | {} | {}\n"] * 3)

def show(p):
    print(board_fmt.format(*[x if x is not None else i for i, x in enumerate(p)]))

def n_move_positions(n):
    marks = list('XOXOXOXOX'[:n]) + ([None] * (9 - n))
    return (p for p in set(permutations(marks, 9)) if game_state(p) )

def game_state(position):
    threes = list({ three_in_a_row(position, line) for line in lines } - { None })
    if len(threes) == 1 and to_play(position) != threes[0]:
        return threes[0]
    elif len(threes) == 0:
        return 'draw' if position.count(None) == 0 else 'in_progress'
    else:
        return False

def three_in_a_row(position, line):
    marks = [ position[i] for i in line if position[i] is not None ]
    return marks[0] if len(marks) == 3 and len(set(marks)) == 1 else None

def to_play(position):
    return 'XO'[position.count('X') - position.count('O')]

def score(position, db):
    state = game_state(position)
    if   state == 'X':           return { 'score':  1, 'moves': None }
    elif state == 'O':           return { 'score': -1, 'moves': None }
    elif state == 'draw':        return { 'score':  0, 'moves': None }
    elif state == 'in_progress': return find_best_score(position, db)
    else: raise Exception("Can't score illegal position {}".format(position))

def find_best_score(position, db):
    player     = to_play(position)
    best_score = None
    moves      = None

    def better(s): return s > best_score if player == 'X' else s < best_score

    for move, p in possible_moves(position):
        score = db[p]['score']
        if best_score is None or better(score):
            best_score = score
            moves = [ move ]
        elif score == best_score:
            moves.append(move)

    return { 'score': best_score, 'moves': moves }

def possible_moves(position):
    mark = to_play(position)
    for i in filter(lambda x: position[x] == None, range(9)):
        new = position[:i] + (mark,) + position[i+1:]
        if game_state(new): yield i, new

def play(db, human, position):
    while game_state(position) == 'in_progress':
        show(position)
        print('{}\n'.format(db[position]))
        if to_play(position) == human:
            move = int(input("Move: "))
        else:
            move = random.choice(db[position]['moves'])
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

def load_db():
    db = {}
    for n in range(9, -1, -1):
        for p in n_move_positions(n):
            db[p] = score(p, db)
    return db

if __name__ == '__main__':
    import sys
    play(load_db(), sys.argv[1], (None,) * 9)
