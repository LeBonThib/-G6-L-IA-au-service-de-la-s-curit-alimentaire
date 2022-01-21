from flask import Blueprint, render_template

adminpanel = Blueprint('adminpanel', __name__)

@adminpanel.route('/admin')
def admin_panel():
    return render_template('adminpanel.html')