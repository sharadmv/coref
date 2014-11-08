import datetime
from functools import wraps

import wtforms_json

from flask import jsonify, request
from webargs import Arg
from webargs.flaskparser import use_args
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from wtforms import validators

from coref import app, auth, db

API_PREFIX = "/api"
wtforms_json.init()

class APIException(Exception):
    def __init__(self, message):
        self.message = message

def handle_error(f):
    @wraps(f)
    def handled(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except APIException as e:
            return jsonify({
                'status': 400,
                'message': e.message
            })
        except Exception:
            import traceback
            print traceback.format_exc()
            return jsonify({
                'status': 500,
                'message': "this is bad"
            })
    return handled

def api_auth(f):
    @wraps(f)
    def handled(*args, **kwargs):
        if current_user.is_authenticated():
            return f(*args, **kwargs)
        else:
            raise APIException("not authenticated")
    return handled

@app.route('/api/fetch')
@handle_error
def fetch():
    return jsonify({
        'id': 1,
        'text': "This character's former lover, Andrea Beaumont, became the Phantasm in one animated movie. Psychologist Chase Meridian falls in love with him and his alter ego in one movie named after this character. Another movie features a crime boss named Carl Grissom and sees another villain fall from a cathedral after attempting to kidnap Vicki Vale; that man is played by Jack Nicholson. A TV series saw Burgess Meredith play the Penguin against Adam West, who played this protagonist. For 10 points, name this comic book character whose most recent movie featured Heath Ledger as The Joker and was called The Dark Knight.",
        'phrases': [
            [0, 14],
            [31, 46]
        ]
    })

@app.route('/api/annotate', methods=['POST'])
@handle_error
@api_auth
def annotate():
    result = request.json
    return jsonify(result)

@app.route('/api/login', methods=['POST'])
@handle_error
def login():
    form = auth.Login.from_json(request.json)
    if not form.validate():
        raise APIException("incorrect parameters")
    try:
        form.validate_login()
        user = form.get_user()
        login_user(user)
        return jsonify({
            'status': 200,
            'message': 'success',
            'data': user.to_dict()
        })
    except validators.ValidationError as e:
        raise APIException(e.message)
    else:
        raise APIException("bad login")


@app.route('/api/register', methods=['POST'])
@handle_error
def register():
    form = auth.Register.from_json(request.json)
    if not form.validate():
        raise APIException("incorrect parameters")
    try:
        form.validate_login()
        user = db.User(
            username=form.username.data,
            password=generate_password_hash(form.password.data),
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            last_login=datetime.datetime.now(),
            is_admin=False
        )
        sess = db.session()
        sess.add(user)
        sess.commit()
        return jsonify({
            'status': 200,
            'message': 'success',
            'data': user.to_dict()
        })
    except validators.ValidationError:
        raise APIException("duplicate login")

@app.route('/api/logout', methods=['POST'])
@handle_error
def logout():
    user = current_user
    logout_user()
    return jsonify({
        'status': 200,
        'message': 'success',
        'data': user.to_dict()
    })

@app.route('/api/test_auth', methods=['GET'])
@login_required
def test_auth():
    return jsonify({
        'status': 200,
        'message': 'success'
    })
