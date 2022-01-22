from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DB_NAME = "alim_confiance.db"

def create_app():
        app = Flask(__name__)
        app.config['SECRET_KEY'] = 'thisisasecretkey' # cookies/session variables encryption

        from .adminpanel import adminpanel
        from .userpanel import userpanel
        from .proto_back import proto_back

        app.register_blueprint(adminpanel, url_prefix='/')
        app.register_blueprint(userpanel, url_prefix='/')
        app.register_blueprint(proto_back, url_prefix='/')

        return app