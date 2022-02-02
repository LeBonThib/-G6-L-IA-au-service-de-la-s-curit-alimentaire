import pandas as pd
import sqlalchemy
import matplotlib as mpl
import pickle
mpl.rcParams['figure.dpi'] = 300
mpl.use('Agg')
from matplotlib import pyplot as plt
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn import model_selection
from sklearn import tree
from sklearn import metrics
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from imblearn.over_sampling import RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler
from collections import Counter
from flask import Blueprint, render_template, flash
from website import db
import os
from time import time
from website import db
start_time = time()
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

proto_ml = Blueprint('proto_ml', __name__)

@proto_ml.route('/proto_ml', methods=['GET','POST'])
def proto_ml_panel():
    """Upon reaching the /proto_ml URL endpoint, call the model_training_module() function.
    Returns:
        function : model_training_module()
    """
    model_training_module()

def model_training_module():
    """The aim of this function is to find the best classification model with some given parameters and then binarize that model for later use in other parts of the application.
    First, we connect to the alim_confiance.db SQLite database via the ORM SQLAlchemy from which we extract data from the tables 'raw_data' and 'inspection_data', we then convert the SQLAlchemy query object to a pandas dataframe for exploitation. 
    Then, we encode the chosen features via the OneHotEncoder encoder and the chosen label via the LabelEncoder, both from the sklearn.preprocessing module; we then fit those encoded data to our feature and label variables. 
    With the train_test_split() function from the sklearn library, we split our dataset into a set of training and testing data. (70/30)
    Now for the fun part, we use our training data within two classification alorithms: a random forest algorithm from the sklearn.ensemble module and a logistic regression algorithm, both with their hyperparameters tuned via cross-validation. (GridSearchCV and StratifiedKFold sklearn.model_selection module)
    We then gather the accuracy score from both models, compare them and pick the model with the highest accuracy score; that model is then binarized via the pickle library and stored as a raw binary file. Once done, we refresh the adminpanel.html template with a message indicating wether or not that process was succesful, which model was picked and its accuracy score.

    Returns:
        function : render_template()
    """
    """ Read raw_data from SQL table """ 
    raw_data_dataframe_query = pd.read_sql_table('raw_data', db.engine)
    raw_data_dataframe = raw_data_dataframe_query

    """ Read inspection_data from SQL table """ 
    inspection_data_dataframe_query = pd.read_sql_table('inspection_data', db.engine)
    inspection_data_dataframe = inspection_data_dataframe_query
    
    feature = raw_data_dataframe.loc[:,["store_zipcode", "store_industry"]]
    label = inspection_data_dataframe['inspection_result']

    feature_encoder = OneHotEncoder()
    label_encoder = LabelEncoder()

    feature = feature_encoder.fit_transform(feature)
    label = label_encoder.fit_transform(label)

    """ Create test and training variables from the base dataframe """ 
    feature_train, feature_test, label_train, label_test = model_selection.train_test_split(feature, label, test_size=0.30, random_state=69)

    """ RANDOM FOREST """ 
    grid_search_classifier = RandomForestClassifier(bootstrap=True, n_jobs=-1)
    params = dict(n_estimators=range(59,86,5))
    print("Starting KFold ...")
    cv_sets = StratifiedKFold(n_splits=10, shuffle=True, random_state=69)
    print("Starting GridSearchCV ...")
    grid_cv = GridSearchCV(grid_search_classifier, params, cv=cv_sets, scoring='accuracy', verbose=1)
    grid_cv.fit(feature_train, label_train)

    best_forest = grid_cv.best_estimator_
    best_forest_result = best_forest.predict(feature_test)
    best_forest_accuracy = metrics.accuracy_score(label_test, best_forest_result)

    """ LOGISTIC REGRESSION  """ 
    logistic_regression = LogisticRegression()
    lr_params = dict(penalty=['none','12'], max_iter=range(1,51,5))
    
    grid_cv_lr = GridSearchCV(logistic_regression, lr_params, cv=cv_sets, scoring='accuracy', verbose=1)
    grid_cv_lr.fit(feature_train, label_train)

    best_lr = grid_cv_lr.best_estimator_
    best_lr_result = best_lr.predict(feature_test)
    best_lr_accuracy = metrics.accuracy_score(label_test, best_lr_result)
    print("--- %s secondes ---" %(time() - start_time))

    """ Compare models, pick most accurate and pass that information to the front  """ 
    best_model, deez_nuts = ((best_lr, f'Modèle entraîné via régression logistique(grid search), accuracy: {int(best_lr_accuracy * 100)}%'), (best_forest, f'Modèle entraîné via random forest(grid search), accuracy: {int(best_forest_accuracy * 100)}%'))[best_forest_accuracy > best_lr_accuracy]
    with open ('/static/model_pickle','wb') as model_file:
        pickle.dump(best_model, model_file)
    with open("/static/encoder_pickle", "wb") as encoder_file: 
        pickle.dump(feature_encoder, encoder_file)
    flash(deez_nuts, category='success')
    return render_template("adminpanel.html")
    