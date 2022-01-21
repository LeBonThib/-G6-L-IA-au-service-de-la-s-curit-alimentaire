from flask import Blueprint, render_template

userpanel = Blueprint('userpanel', __name__)

@userpanel.route('/')
def user_panel():
    return render_template('userpanel.html')