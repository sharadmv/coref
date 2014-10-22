from flask import jsonify, request
from webargs import Arg
from webargs.flaskparser import use_args

from coref import app

API_PREFIX = "/api"

@app.route('/api/fetch')
def fetch():
    return jsonify({
        'id': 1,
        'text': "This character's former lover, Andrea Beaumont, became the Phantasm in one animated movie. Psychologist Chase Meridian falls in love with him and his alter ego in one movie named after this character. Another movie features a crime boss named Carl Grissom and sees another villain fall from a cathedral after attempting to kidnap Vicki Vale; that man is played by Jack Nicholson. A TV series saw Burgess Meredith play the Penguin against Adam West, who played this protagonist. For 10 points, name this comic book character whose most recent movie featured Heath Ledger as The Joker and was called The Dark Knight.",
        'phrases': [
            [0, 16],
            [25, 29]
        ]
    })

@app.route('/api/annotate', methods=['POST'])
def annotate():
    result = request.json
    return jsonify(result)
