from flask import Flask, url_for

def create_app():
        app = Flask(__name__)
        app.config['SECRET_KEY'] = 'thisisasecretkey' # cookies/session variables encryption

        from .adminpanel import adminpanel
        from .userpanel import userpanel

        app.register_blueprint(adminpanel, url_prefix='/')
        app.register_blueprint(userpanel, url_prefix='/')

        return app
