from flask import Flask
app = Flask(__name__, template_folder="../templates", static_folder='../static')
app.secret_key = "A0Zr98j/3yX R~XHH!jmN]LWX/,?RT"

import db

import auth
import urls
import api

def listen(port=8080, debug=True):
    app.debug = True
    app.run(port=port)
