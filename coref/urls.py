import datetime
import json

from flask import render_template, session

from coref import app, auth, db
from flask_login import current_user

@app.route('/')
def index():
    session["logged_in"] = json.dumps(current_user.is_authenticated())
    session["user"] = json.dumps(current_user.to_dict())
    return render_template('index.html')
