from flask import Flask
app = Flask(__name__, template_folder="../templates", static_folder='../static')

import urls
import api

def listen(port=8080, debug=True):
    app.debug = True
    app.run(port=port)
