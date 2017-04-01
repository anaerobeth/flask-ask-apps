import logging
from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

app = Flask(__name__)
ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

@ask.launch
def new_game():
    welcome_msg = render_template('welcome')
    return question(welcome_msg)

@ask.intent("YesIntent")
def next_round():
    opening = "King's Indian Defense"
    moves = [['e4', 'e5'], ['d4', 'Knight f6']]
    target = ['white e pawn', 'e', 4]
    session.attributes['target_pawn'] = target[0]
    session.attributes['target_row'] = target[2]
    round_msg = render_template('round', opening=opening, moves=moves, target=target)
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

