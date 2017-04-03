import logging
from random import choice
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

app = Flask(__name__)
ask = Ask(app, "/")

openings = [
    {"name": "Quiet Game", "moves": [[ "e4", "e5" ], [ "Knight f3", "Knight c6" ], [ "Bishop c4", "Bishop c5"]], "target": [ "white e pawn", 4 ]},
    {"name": "Evan's Gambit", "moves": [[ "e4", "e5" ], [ "Knight f3", "Knight c6" ], [ "Bishop c4", "Bishop c5"], [ "b4", ""]], "target": [ "black b pawn", 7 ]},
    {"name": "Ruy Lopez", "moves": [[ "e4", "e5" ], [ "Knight f3", "Knight c6" ], [ "Bishop b5", "" ]], "target": [ "white e pawn", 4 ]},
    {"name": "Guioco Pianissimo", "moves": [[ "e4", "e5" ], [ "Knight f3", "Knight c6" ], [ "Bishop c4", "Bishop c5"], [ "d3","" ]], "target": [ "black c pawn", 2]},
    {"name": "King's Gambit", "moves": [[ "e4", "e5" ], [ "f4", "" ]], "target": [ "black e pawn", 5]},
    {"name": "Sicilian Defense Dragon Variation", "moves": [[ "e4", "c5" ], [ "Knight f3", "d6" ], [ "d4", "c takes d4",], [ "Knight takes d4", "Knight f6"], [ "Knight c3", "g6"]], "target": [ "black d pawn", 6]},
    {"name": "Sicilian Defense Najdorf Variation", "moves": [[ "e4", "c5" ], [ "Knight f3", "d6" ], [ "d4", "c takes d4",], [ "Knight takes d4", "Knight f6"], [ "Knight c3", "a6" ]], "target": [ "white e pawn", 4 ]},
    {"name": "French Defense", "moves": [[ "e4", "e6" ], [ "d4", "d5"]], "target": [ "black e pawn", 6]},
    {"name": "Caro-Kann", "moves": [[ "e4", "c6" ], [ "d4", "d5"]], "target": [ "white  d pawn", 4]},
    {"name": "Caro-Kann Main Line", "moves": [[ "e4", "c6" ], [ "d4", "d5"], [ "Knight c3", "d takes e4"]], "target": [ "black c pawn", 6]},
    {"name": "Center Counter", "moves": [[ "e4", "d5" ], ["e takes d5", "Queen takes d5"]], "target": [ "white d pawn", 2]},
    {"name": "Modern Defense", "moves": [[ "e4", "g6" ], [ "d4", "Bishop g7"]], "target": [ "black d pawn", 7]},
    {"name": "Queen's Gambit Accepted", "moves": [[ "d4", "d5" ], [ "c4", "d takes c4"]], "target": [ "white d pawn", 4 ]},
    {"name": "Queen's Gambit Tarrasch Defense", "moves": [[ "d4", "d5" ], [ "c4", "e6"]], "target": [ "black e pawn", 6]},
    {"name": "Queen's Gambit Chigorin Defense", "moves": [[ "d4", "d5" ], [ "c4", "Knight c6"]], "target": [ "black d pawn", 5 ]},
    {"name": "King's Indian Defense", "moves": [[ "d4", "Knight f6" ], [ "c4", "g6" ], [ "Knight c3", "Bishop g7"]], "target": [ "white c pawn", 4]},
    {"name": "Nimzo-Indian Defense", "moves": [[ "d4", "Knight f6" ], [ "c4", "e6"], [ "Knight c3", "Bishop b4" ]], "target": [ "black e pawn", 6 ]}
]

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

@ask.launch
def new_game():
    welcome_msg = render_template('welcome')
    return question(welcome_msg)

@ask.intent("YesIntent")
def next_round():
    opening = choice(openings)
    name = opening["name"]
    moves = opening["moves"]
    target = opening["target"]
    second_move, third_move, fourth_move, fifth_move = '', '', '', ''
    session.attributes['target_pawn'] = target[0]
    session.attributes['target_row'] = target[1]

    challenge = "{name}. First move, {moves[0][0]}, {moves[0][1]}".format(name=name, moves=moves)
    if len(moves) > 1:
        second_move = "Second move, {moves[1][0]}, {moves[1][1]}".format(moves=moves)
    if len(moves) > 2:
        third_move = "Third move, {moves[2][0]}, {moves[2][1]}".format(moves=moves)
    if len(moves) > 3:
        fourth_move = "Fourth move, {moves[3][0]}, {moves[3][1]}".format(moves=moves)
    if len(moves) > 4:
        fifth_move = "Fifth move, {moves[4][0]}, {moves[4][1]}".format(moves=moves)
    target = "Where is the {target[0]}?".format(target=target)
    print(challenge)

    round_msg = render_template('round', challenge=challenge, second_move=second_move, third_move=third_move, fourth_move=fourth_move, fifth_move=fifth_move, target=target)

    return question(round_msg)

@ask.intent("AnswerIntent", convert={'second': int})
def answer(first, second):
    pawn = session.attributes['target_pawn']
    row = session.attributes['target_row']

    if second == row:
        msg = render_template('win', pawn=pawn, row=row)
    else:
        msg = render_template('lose', pawn=pawn, row=row)
    return statement(msg)

if __name__ == '__main__':
    app.run(debug=True)

