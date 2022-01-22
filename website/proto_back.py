from flask import Blueprint, render_template

proto_back = Blueprint('proto_back', __name__)

@proto_back.route('/proto_back')
def proto_back():
    return render_template('proto_back.html')