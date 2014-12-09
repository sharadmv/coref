import datetime
from functools import wraps

import wtforms_json

from flask import jsonify, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from wtforms import validators

from coref import app, auth, db

API_PREFIX = "/api"
wtforms_json.init()

class APIException(Exception):
    def __init__(self, message, code=400):
        self.message = message
        self.code = code

def handle_error(f):
    @wraps(f)
    def handled(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except APIException as e:
            return jsonify({
                'status': e.code,
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
    with db.session() as session:
        if current_user.is_authenticated():
            mention_pairs = list(session.query(db.MentionPair).join(db.Question.mention_pairs).outerjoin(db.MentionPair.user_mention_pairs).filter(
                db.Coref.mention_pair_id == None
            ).order_by(db.Question.score.desc()).order_by(db.MentionPair.score.desc()))
            if len(mention_pairs) > 0:
                question = mention_pairs[0].question
                pairs = [mp.to_dict() for mp in mention_pairs if mp.question_id == question.question_id]
                return jsonify({
                    'question': question.to_dict(),
                    'mention_pairs': pairs
                })
            return jsonify({
                'question': None,
                'mention_pairs': []
            })
        else:
            mention_pairs = list(session.query(db.MentionPair).join(db.Question.mention_pairs).outerjoin(db.MentionPair.user_mention_pairs).order_by(db.Question.score.desc()).order_by(db.MentionPair.score.desc()))
            if len(mention_pairs) > 0:
                question = mention_pairs[0].question
                pairs = [mp.to_dict() for mp in mention_pairs if mp.question_id == question.question_id]
                return jsonify({
                    'question': question.to_dict(),
                    'mention_pairs': pairs
                })
        return jsonify({
            'question': None,
            'mention_pairs': []
        })

@app.route('/api/annotate', methods=['POST'])
@handle_error
@api_auth
def annotate():
    result = request.json
    with db.session() as session:
        existing = session.query(db.Coref).filter(
            db.Coref.author == current_user.user_id,
            db.Coref.mention_pair_id == result['mention_pair_id']
        )
        if len(list(existing)) == 0:
            coref = db.Coref(question_id=result['question_id'],
                            mention_pair_id=result['mention_pair_id'],
                            same=result['result'],
                            author=current_user.user_id
                            )
            session.add(coref)
            session.commit()
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
        print "User", user
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
        with db.session() as session:
            user = db.User(
                username=form.username.data,
                password=generate_password_hash(form.password.data),
                email=form.email.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                last_login=datetime.datetime.now(),
                is_admin=False
            )
            session.add(user)
            session.commit()
            login_user(user)
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
