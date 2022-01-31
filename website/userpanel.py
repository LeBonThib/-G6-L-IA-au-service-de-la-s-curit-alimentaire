from flask import Blueprint, render_template, request, flash
import pandas as pd
import pickle

userpanel = Blueprint('userpanel', __name__)
from .models import raw_data

@userpanel.route('/', methods=['GET', 'POST'])
def user_panel():
    list_industry = get_industries_from_db()
    max_industry = len(list_industry)

    if request.method == 'POST':
        form_check_for_prediction = request.form
        if form_check_for_prediction.get('prediction_button'):
            store_zipcode = form_check_for_prediction.get('store_zipcode')
            store_industry = form_check_for_prediction.get('store_industry')
            if store_zipcode == '12345':
                flash("Haha, très drôle, tu es vraiment un petit rigolo.", category='error')
                return render_template('userpanel.html', list_industry_param=list_industry, max_industry_param=max_industry)
            if len(store_zipcode) != 5:
                flash("Code Postal doit faire exactement 5 caractères.", category='error')
                return render_template('userpanel.html', list_industry_param=list_industry, max_industry_param=max_industry)
            if not store_zipcode.isnumeric():
                flash("Fais pas le malin, utilise des chiffres.", category='error')
                return render_template('userpanel.html', list_industry_param=list_industry, max_industry_param=max_industry)
            model_prediction_module(store_zipcode, store_industry)

    return render_template('userpanel.html', list_industry_param=list_industry, max_industry_param=max_industry)

def get_industries_from_db():
    industry_query = raw_data.query.with_entities(raw_data.store_industry).distinct()
    industry_list = []
    for industry in industry_query:
        industry_list.append(industry[0])
    industry_list.sort()
    return industry_list

def model_prediction_module(store_zipcode, store_industry):
    with open('model_pickle','rb') as model_file:
        loaded_model = pickle.load(model_file)
    with open('encoder_pickle','rb') as encoder_file:
        loaded_encoder = pickle.load(encoder_file)

    feature_dict = dict(store_zipcode = str(float(store_zipcode)), store_industry = store_industry)
    feature_data = pd.DataFrame(feature_dict, index=[0])
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