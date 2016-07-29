import flask
from flask import Blueprint
from flask_login import (LoginManager, login_required, login_user,
                         current_user, logout_user, UserMixin)

from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired
from ..models import db, User

from datetime import datetime
import sys

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    print "before form validate"
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        user = User.get_by_email(form.email.data)
        print "before login_user %s" % user

        login_user(user)
        print "after login_user"
        flask.flash('Logged in successfully.')

        next_url = flask.request.args.get('next')
        print "before next validate"

        if not next_is_valid(next_url):
            return flask.abort(400)
        print "before redirect"

        return flask.redirect(next_url or flask.url_for('index'))
    return flask.render_template('login.html', form=form)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(somewhere)

def next_is_valid(url):
    # TODO(snaik): check if the user has valid permission to access the `next` url
    return True

def generate_login_token(user_id, email, password):
    return str(user_id) + sha256_crypt.encrypt(email + password)

def create_confirmed_user(email, number, password, first_name=None, last_name=None, org=None):
    print "create confirmed user %s" % email

    # Check if we have a user for this email already
    user = User.query \
        .filter(User.email == email) \
        .scalar()
    print "existing user found? %s" % user

    try:
        new_user = not user
        if user is None:
            user = User(email, number, password)
            db.session.add(user)
        print "created user %s" % user

        user.date_confirmed = datetime.utcnow()
        print "before save %s" % user

        db.session.commit()
        print "saved user %s" % email

        # If everything worked, log the user in.
        # login_user(user, remember=True)

    except AttributeError as err:
        print("AttributeError : {0}".format(err))
        db.session.rollback()
        logout_user()
        raise

    db.session.close()

    return user

class LoginForm(Form):
    email = TextField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])

    def validate(self):
        user = self.get_user()
        print "LoginForm user = %s" % user
        if user is None or not user.check_password(self.password.data):
            self.email.errors.append('Invalid credentials')
            return False
        # if get_email_domain(user.email) != "clementineinc.com":
        #     self.email.errors.append('Only Clementine employees allowed to login')
        #     return False
        
        return True
           
    def get_user(self):
        return User.query.filter(User.email==self.email.data, User.date_confirmed != None).scalar()
