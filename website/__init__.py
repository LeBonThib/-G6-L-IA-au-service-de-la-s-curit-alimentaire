from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from os import path

# DATABASE PARAMS
db = SQLAlchemy()
DB_NAME = "alim_confiance.db"

def create_app():
        """
        This function allows for the instantiation of the core flask class. 
        It takes parameters via the 'config' method. The flask class requires one mandatory parameter : 'SECRET_KEY' which is used to sign session cookies for protection against cookie data tampering. (used through the flask.session module). We also add two extra parameters, 'SQLALCHEMY_DATABASE_URI', which is the locator for the SQLite database file and 'SQL_ALCHEMY_TRACK_MODIFICATIONS' which tracks modifications of objects. Since we do not need the Flask event system for this project, we decided to disable this functionality as to reduce overhead memory usage. (https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/)

        Returns:
                <class 'flask.app.Flask'>: A Flask application object with parameters.
        """
        app = Flask(__name__)
        app.config['SECRET_KEY'] = 'thisisasecretkey' # cookies/session variables encryption
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(app)

        """ Establish application routes """
        from .adminpanel import adminpanel
        from .userpanel import userpanel
        from .proto_back import proto_back
        from .proto_ml import proto_ml

        """ Establish application blueprints """
        app.register_blueprint(adminpanel, url_prefix='/')
        app.register_blueprint(userpanel, url_prefix='/')
        app.register_blueprint(proto_back, url_prefix='/')
        app.register_blueprint(proto_ml, url_prefix='/')

        """ Establish database structure """
        from .models import raw_data, inspection_data, logs #training_data

        """ Call create_database() """
        create_database(app)

        return app
        
def create_database(app):
        """This function allows for the creation of an empty SQLite database if none exist already in the application files according to the structure as laid out in the models.py file.

        Args:
                app (<class 'flask.app.Flask'>): Instantiated flask class containing database parameters from the models file.
        """
        if not path.exists('website/' + DB_NAME):
                db.create_all(app=app)
                print('Created Database!')