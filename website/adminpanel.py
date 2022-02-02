from flask import Blueprint, render_template, request, flash
from .proto_back import refresh_and_rebase
from .proto_ml import model_training_module

adminpanel = Blueprint('adminpanel', __name__)

@adminpanel.route('/admin', methods=['POST','GET'])
def admin_panel():
    """Upon reaching the /admin URL endpoint, renders the adminpanel.html template. Upon receiving data via the POST method, calls one of two functions, depending on the value of the form : refresh_and_rebase() (from proto_back.py) or model_training_module() (from proto_ml.py).

    Returns:
        function : render_template()
    """
    if request.method == 'POST':
        form_check_for_resfresh = request.form
        if form_check_for_resfresh.get('refresh_csv'):
            refresh_and_rebase()
        elif form_check_for_resfresh.get('retrain_model'):
            model_training_module()
        else:
            flash("Could not access refresh_and_rebase module.", category='error')
            return render_template('adminpanel.html')
    return render_template('adminpanel.html')