from flask import Blueprint, render_template

proto_back = Blueprint('proto_back', __name__)

@proto_back.route('/proto_back')
def proto_back_panel():
    return render_template('proto_back.html')