from flask import Flask, render_template, session, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle

app = Flask(__name__)

# for testing NOT developing
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

app.config['SECRET_KEY'] = '12345'
debug = DebugToolbarExtension(app)

boggle_game = Boggle()
guesses = set()

@app.route('/')
def show_board():
    """ Sets up and shows the board game """

    boggle_board = boggle_game.make_board()
    session["board"] = boggle_board
    return render_template('board.html', board=boggle_board)

def check_guess_validity(guess):
    """ Checks the validity of the guessed word, then returns a msg
    - if word exists and is on board: msg => "ok" or msg => "word-already-used" (if used before)
    - if word exists but not on board: msg => "not-on-board"
    - if word doesnt exist: msg => "not-word"
    """

    msg = boggle_game.check_valid_word(session['board'], guess)
    if msg == "ok":
        if guess in guesses:
            msg = "word-already-used"
        else:
            guesses.add(guess)
    
    return msg


@app.route('/', methods=['POST'])
def submit_guess():
    """ Receives a guess and checks its validity, then responds with a msg """

    guess = request.get_json().get('guess', ' ')
    msg = check_guess_validity(guess)
    response = { "result": msg }
    return jsonify(response)

def update_user_stats(score):
    """ Helper function: updates high_score & played_games after each game """

    played = session.get('played', 0) + 1
    session['played'] = played

    if session.get('high_score') or session.get('high_score') == 0:
        if score > session['high_score']:
            session['high_score'] = score
    else:
        session['high_score'] = score

@app.route('/endgame', methods=['POST'])
def get_user_stats():
    """ Receives the user's score at the end of the game, updates high_score & played_games, then sends it back """

    score = request.get_json().get('score')
    update_user_stats(score)
    response = { "high_score": session['high_score'], "played": session['played'] }
    return jsonify(response)