import logging
from random import choice
from string import ascii_letters
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

app = Flask(__name__)
ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

@ask.launch
def new_game():
    first_fact = render_template(choice(ascii_letters))
    welcome_msg = render_template('welcome', first_fact=first_fact)
    return question(welcome_msg)

@ask.intent("YesIntent")
def next_round():
    second_fact = render_template(choice(ascii_letters))
    round_msg = render_template('round', second_fact=second_fact)
    return statement(round_msg)

if __name__ == '__main__':
    app.run(debug=True)

