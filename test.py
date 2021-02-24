from unittest import TestCase
from app import app, check_guess_validity, guesses, update_user_stats
from flask import session, request, json
from boggle import Boggle


class FlaskTests(TestCase):

    @classmethod
    def setUpClass(cls):
        """ Instantiates the game and sets guesses to an empty set before any test method is run """

        cls.boggle_game = Boggle()
        cls.guesses = guesses

    def test_show_board(self):
        """ Tests the show_board view """

        with app.test_client() as client:
            response = client.get('/')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<table id="boggle-board">', html)
            self.assertEqual(len(session['board']), 5)

    def test_check_guess_validity(self):
        """ Tests the check_guess_validity helper function from app.py """

        with app.test_client() as client:
            response = client.get('/')

            # change board letters to something we can test
            session['board'] = [
                ['A', 'a', 'a', 'a', 'a'],
                ['A', 'a', 'a', 'a', 'a'],
                ['A', 'a', 'a', 'a', 'a'],
                ['A', 'a', 'a', 'a', 'a'],
                ['A', 'a', 'a', 'a', 'a']
            ]

            # Test that its case sensitive
            self.assertEqual(check_guess_validity('A'), 'ok')
            self.assertEqual(check_guess_validity('a'), 'ok')

            # Check guesses that aren't words
            self.assertEqual(check_guess_validity('aaa'), 'not-word')

            # Check guesses that aren't on the board
            self.assertEqual(check_guess_validity('word'), 'not-on-board')

            # Test that valid guesses get added to set and invalid ones dont
            self.assertTrue('A' in self.guesses and 'a' in self.guesses)
            self.assertTrue('aaa' not in self.guesses and 'word' not in self.guesses)

            # Test valid guesses that are being repeated
            self.assertEqual(check_guess_validity('A'), 'word-already-used')

    def test_submit_guess(self):
        """ Tests the submission of guesses to the API """

        with app.test_client() as client:
            # just to get session['board'] (can do it manually, but this is easier)
            client.get('/')

            response = client.post('/', 
            data=json.dumps({ "guess": "word" }), 
            content_type='application/json')

            # Test that it goes through and we get a response back with "result" data
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.get_json().get('result'))

    def test_update_user_stats(self):
        """ Tests the update_user_stats helper function from app.py
        - score gets parsed to an integar in app.js (no need to test strings here)
        """

        with app.test_client() as client:
            client.get('/')

            # 1st game ends
            update_user_stats(2)
            # check if stats got initialized
            self.assertEqual(session['played'], 1)
            self.assertEqual(session['high_score'], 2)

            # 2nd game ends
            update_user_stats(8)
            # check if stats got updated
            self.assertEqual(session['played'], 2)
            self.assertEqual(session['high_score'], 8)

    def test_end_game(self):
        """ Tests the submission of user stats post game """

        with app.test_client() as client:
            response = client.post('/endgame', 
            data=json.dumps({ "score": 2 }),
            content_type='application/json')

            # Check if it goes through and we get a response back with "high_score" and "played" data
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.get_json().get('high_score') and response.get_json().get('played'))