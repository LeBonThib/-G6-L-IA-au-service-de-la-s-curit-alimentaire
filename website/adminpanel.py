from flask import Blueprint, render_template, request, flash
from .proto_back import refresh_and_rebase

adminpanel = Blueprint('adminpanel', __name__)

@adminpanel.route('/admin', methods=['POST','GET'])
def admin_panel():
    if request.method == 'POST':
        form_check_for_resfresh = request.form
        if form_check_for_resfresh.get('refresh_csv'):
            refresh_and_rebase()
        else:
            flash("Could not access refresh_and_rebase module.", category='error')
            return render_template('adminpanel.html')
    return render_template('adminpanel.html')