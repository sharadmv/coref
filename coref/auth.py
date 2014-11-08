from wtforms import form, fields, validators
from flask_login import LoginManager, UserMixin
from werkzeug.security import check_password_hash

from flask.ext.login import AnonymousUserMixin

from coref import app
from coref.db import User, session

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return session().query(User).get(user_id)

class Anonymous(AnonymousUserMixin):
    def __init__(self):
        self.username = 'Guest'

    def to_dict(self):
        return {}

login_manager.anonymous_user = Anonymous




class Login(form.Form):
    username = fields.TextField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('Invalid username or password')

        if not check_password_hash(user.password, self.password.data):
            raise validators.ValidationError('Invalid username or password')

    def get_user(self):
        return session().query(User).filter_by(username=self.username.data).first()


class Register(form.Form):
    username = fields.TextField(validators=[validators.required()])
    first_name = fields.TextField(validators=[validators.required()])
    last_name = fields.TextField(validators=[validators.required()])
    email = fields.TextField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self):
        if session().query(User).filter_by(username=self.username.data).count() > 0:
            raise validators.ValidationError('duplicate username')
