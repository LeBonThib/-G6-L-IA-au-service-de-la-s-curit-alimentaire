from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "alim_confiance.db"

def create_app():
        app = Flask(__name__)
        app.config['SECRET_KEY'] = 'thisisasecretkey' # cookies/session variables encryption
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(app)

        from .adminpanel import adminpanel
        from .userpanel import userpanel
        from .proto_back import proto_back
        from .proto_ml import proto_ml

        app.register_blueprint(adminpanel, url_prefix='/')
        app.register_blueprint(userpanel, url_prefix='/')
        app.register_blueprint(proto_back, url_prefix='/')
        app.register_blueprint(proto_ml, url_prefix='/')

        from .models import raw_data, inspection_data, logs, training_data

        create_database(app)

        return app

def create_database(app):
        if not path.exists('website/' + DB_NAME):
                db.create_all(app=app)
                print('Created Database!')