from flask import Flask, render_template, session, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from flask_cors import CORS, cross_origin
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'

CORS(app, resources=r'/*')

debug = DebugToolbarExtension(app)

boggle_game = Boggle()

@app.route('/')
def show_board():
    boggle_board = boggle_game.make_board()
    session["board"] = boggle_board
    return render_template('board.html', board=boggle_board)

def check_valid_word(word):
    msg = boggle_game.check_valid_word(session['board'], word)
    return msg

@app.route('/', methods=['POST'])
@cross_origin(allow_headers=['Content-Type'])
def submit_guess():
    guess = request.get_json().get('guess', '')
    response = {"result": check_valid_word(guess)}
    return jsonify(response)