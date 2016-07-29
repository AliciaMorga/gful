import logging

from flask import current_app, Flask, redirect, url_for
from flask_login import LoginManager
from models import User

def create_app(config, debug=False, testing=False, config_overrides=None):
    app = Flask(__name__)
    app.config.from_object(config)

    app.debug = debug
    app.testing = testing

    # Load configs
    if config_overrides:
        app.config.update(config_overrides)

    # Configure logging
    if not app.testing:
        logging.basicConfig(level=logging.INFO)

    # Setup the data model.
    with app.app_context():
        import models 
        models.init_app(app)

    ## Flask-login init
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "/login"

    # Register blueprints
    from controllers.auth import auth
    from controllers.customer_admin import customer_admin
    from controllers.users import users
    from controllers.groups import groups
    from controllers.search import search
    from controllers.sms import sms

    app.register_blueprint(auth)
    app.register_blueprint(customer_admin, url_prefix='/a')
    app.register_blueprint(users, url_prefix='/users')
    app.register_blueprint(groups, url_prefix='/groups')
    app.register_blueprint(search, url_prefix='/search')
    app.register_blueprint(sms, url_prefix='/sms')

    # flask-login implementation
    @login_manager.user_loader
    def load_user_with_id(user_id):
        return User.query.get(user_id)

    # Add a default root route.
    @app.route("/")
    def index():
        return redirect(url_for('customer_admin.home'))

    # Add an error handler. This is useful for debugging the live application,
    # however, you should disable the output of the exception for production
    # applications.
    @app.errorhandler(500)
    def server_error(e):
        return """
        An internal error occurred: <pre>{}</pre>
        See logs for full stacktrace.
        """.format(e), 500

    return app

