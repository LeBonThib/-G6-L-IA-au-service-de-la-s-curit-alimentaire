from flask import Blueprint, render_template, request, flash
import pandas as pd
import pickle
from sqlalchemy import text
from website import db
import os

userpanel = Blueprint('userpanel', __name__)
from .models import raw_data

@userpanel.route('/', methods=['GET', 'POST'])
def user_panel():
    """Upon reaching the / URL endpoint, renders the userpanel.html template. Upon receiving data via the POST method, we collect data from the form in different variables and run checks to ensure that the received data fits the desired format, as well as handle the odd edge case. If any of those checks does not pass, we refresh the userpanel.html template with information as to why this process failed. If all checks pass, call the model_prediction_module() function.

    Returns:
        function : render_template() - 
    """
    list_industry = get_industries_from_db()
    max_industry = len(list_industry)

    if request.method == 'POST':
        form_check_for_prediction = request.form
        if form_check_for_prediction.get('prediction_button'):
            store_zipcode = form_check_for_prediction.get('store_zipcode')
            store_industry = form_check_for_prediction.get('store_industry')
            find_model_check = 'website/model_pickle'
            find_encoder_check = 'website/encoder_pickle'
            if not os.path.exists(find_model_check):
                flash("Pas de modèle détecté, merci de bien vouloir entraîner un modèle de classification depuis le panel admin.", category='error')
                return render_template('userpanel.html', list_industry_param=list_industry, max_industry_param=max_industry)
            if not os.path.exists(find_encoder_check):
                flash("Pas de modèle détecté, merci de bien vouloir entraîner un modèle de classification depuis le panel admin.", category='error')
                return render_template('userpanel.html', list_industry_param=list_industry, max_industry_param=max_industry)
            if store_zipcode == '12345':
                flash("Haha, très drôle, tu es vraiment un petit rigolo.", category='error')
                return render_template('userpanel.html', list_industry_param=list_industry, max_industry_param=max_industry)
            if len(store_zipcode) != 5:
                flash("Code Postal doit faire exactement 5 caractères.", category='error')
                return render_template('userpanel.html', list_industry_param=list_industry, max_industry_param=max_industry)
            if not store_zipcode.isnumeric():
                flash("Fais pas le malin, utilise des chiffres.", category='error')
                return render_template('userpanel.html', list_industry_param=list_industry, max_industry_param=max_industry)
            model_prediction_module(store_zipcode, store_industry, list_industry, max_industry)

    return render_template('userpanel.html', list_industry_param=list_industry, max_industry_param=max_industry)

def get_industries_from_db():
    """The aim of this function is to pass a list containing data queried from the 'store_industry' column from the 'raw_data' table to the userpanel.html template to be used in a <select> tag in the main form. 

    Returns:
        industry_list : list
    """
    industry_query = raw_data.query.with_entities(raw_data.store_industry).distinct()
    industry_list = []
    for industry in industry_query:
        industry_list.append(industry[0])
    industry_list.sort()
    return industry_list

def model_prediction_module(store_zipcode, store_industry, list_industry, max_industry):
    """The aim of this function is to apply the pickled_model generated in the model_training_module() function with the parameters inputted by the user in the form from the userpanel.html template.
    First we 


    Returns:
        industry_list : list
    """
    with open('model_pickle','rb') as model_file:
        loaded_model = pickle.load(model_file)
    with open('encoder_pickle','rb') as encoder_file:
        loaded_encoder = pickle.load(encoder_file)

    feature_dict = dict(store_zipcode = str(float(store_zipcode)), store_industry = store_industry)
    feature_data = pd.DataFrame(feature_dict, index=[0])
    zipcode_check_query = text(f'SELECT * FROM raw_data WHERE store_zipcode = {str(float(store_zipcode))}')
    zipcode_check_return = pd.read_sql_query(zipcode_check_query, db.engine)
    if zipcode_check_return.empty:
        flash("Ce code postal n'est pas dans la base de données, je ne peux donc pas faire de prédiction.", category='error')
        return render_template('userpanel.html', list_industry_param=list_industry, max_industry_param=max_industry)
    feature_test = loaded_encoder.transform(feature_data)
    prediction = loaded_model.predict(feature_test) 
    
    if prediction[0] == 0:
        flash("Prédiction: À améliorer, je serais toi, j'irais faire un tour quand même.", category='success')
    if prediction[0] == 1:
        flash("Prédiction: À corriger de manière urgente, lâche tout, appelle la police, ils sont probablement en train de cuisiner des chats.", category='success')
    if prediction[0] == 2:
        flash("Prédiction: Très Satisfaisant, même pas besoin d'y aller, fais confiance tkt maggle.", category='success')
    if prediction[0] == 3:
        flash("Prédiction: Satisfaisant, c'est pas urgent urgent mais les oublie pas, bisous.", category='success')