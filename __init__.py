import os
from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.databaseConfig = {
        'host': '10.10.1.25',
        'port': 3306,
        'user': 'root',
        'password': '3eaSss*7',
        'database': 'gehs_db'
        }
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE={
        'host': '10.10.1.25',
        'port': 3306,
        'user': 'root',
        'password': '3eaSss*7',
        'database': 'gehs_db'
        },
        PORT='3306',
        USER='root',
        PASSWORD='3eaSss*7',
        HOST='10.10.1.25'
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    from . import db
    db.init_app(app)
    
    from . import dash
    app.register_blueprint(dash.bp)
    app.add_url_rule('/', endpoint='index')

    return app