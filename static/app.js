const $guessForm = $('#guess-form'),
    $guess = $('#word'),
    $score = $('#score'),
    $timer = $('#timer');

class FlaskBoggle {
    constructor() {
        this.baseUrl = 'http://localhost:5000';
    }

    /* Alerts user of guess validity, updates current score if word is valid, then resets guess form */
    updateUI(result, word) {
        alert(`${word}: ${result}`);
        if (result === 'ok') {
            $score.text(parseInt($score.text()) + word.length);
        };
        $guessForm.trigger('reset');
    }

    /* Submits the user's guess to the API */
    async submitGuess(evt) {
        evt.preventDefault();
        const word = $guess.val();
        const res = await axios({
            url: this.baseUrl,
            method: "POST",
            data: { guess: word }
        });
        this.updateUI(res.data.result, word);
    }

    /* Sends the user's round score to the API (at end of game) */
    async sendUserStats() {
        const res = await axios({
            url: `${this.baseUrl}/endgame`,
            method: "POST",
            data: { score: parseInt($score.text()) }
        });
        console.log(res.data);
    }
}

$(function() {
    // init function
    const app = new FlaskBoggle();
    $guessForm.on('submit', (evt) => app.submitGuess.call(app, evt));

    // After 60 seconds, ends game and sends score to API
    setTimeout(function() {
        $guessForm.addClass('hidden');
        $timer.removeClass('hidden');
        app.sendUserStats();
    }, 60000)
});