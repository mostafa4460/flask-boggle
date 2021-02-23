const apiURL = 'http://localhost:5000';
const $guessForm = $('#guess-form'),
    $guess = $('#word');

async function submitGuess(evt) {
    evt.preventDefault();
    const word = $guess.val();
    const res = await axios({
        url: `${apiURL}`,
        method: "POST",
        headers: {  
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        data: { guess: word }
    });
    console.log(res)
    $guessForm.trigger('reset');
}

$guessForm.on('submit', submitGuess);