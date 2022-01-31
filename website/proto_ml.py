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
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler
from collections import Counter
from flask import Blueprint, render_template
from website import db
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

proto_ml = Blueprint('proto_ml', __name__)

@proto_ml.route('/proto_ml', methods=['GET','POST'])
def proto_ml_panel():
    model_training_module()
    return render_template("adminpanel.html")

def model_training_module():
    # Create the engine to connect to the database
    engine = sqlalchemy.create_engine('sqlite:///C:\\Users\\Pontiff\\Desktop\\SIMPLON_DEV_IA_DOCUMENTS_THIBAUT_PERNET\\-G6-L-IA-au-service-de-la-s-curit-alimentaire\\website\\alim_confiance.db')
    
    # Read raw_data from SQL table
    raw_data_dataframe_query = pd.read_sql_table('raw_data', engine)
    raw_data_dataframe = raw_data_dataframe_query

    # Read inspection_data from SQL table
    inspection_data_dataframe_query = pd.read_sql_table('inspection_data', engine)
    inspection_data_dataframe = inspection_data_dataframe_query
    
    feature = raw_data_dataframe.loc[:,["store_zipcode", "store_industry"]]
    label = inspection_data_dataframe['inspection_result']

    print(type(feature))
    print(feature.info())

    feature_encoder = OneHotEncoder()
    label_encoder = LabelEncoder()

    feature = feature_encoder.fit_transform(feature)
    label = label_encoder.fit_transform(label)

    """ # Create the sampler
    oversampler = RandomOverSampler(sampling_strategy='minority')
    feature_resampled, label_resampled = oversampler.fit_resample(feature, label)

    # Compare label classes to check sampling result.
    print(f'Label brut:\n{Counter(label)}')
    print(f'Label resampled:\n{Counter(label_resampled)}')

    # Create test and training variables from the oversampled dataframe
    feature_train, feature_test, label_train, label_test = model_selection.train_test_split(feature_resampled, label_resampled, test_size=0.30, random_state=69) """

    """ # Create the sampler
    oversampler = RandomUnderSampler(sampling_strategy='majority')
    feature_resampled, label_resampled = oversampler.fit_resample(feature, label)

    # Compare label classes to check sampling result.
    print(f'Label brut:\n{Counter(label)}')
    print(f'Label resampled:\n{Counter(label_resampled)}')

    # Create test and training variables from the undersampled dataframe
    feature_train, feature_test, label_train, label_test = model_selection.train_test_split(feature_resampled, label_resampled, test_size=0.30, random_state=69) """

    # Create test and training variables from the base dataframe
    feature_train, feature_test, label_train, label_test = model_selection.train_test_split(feature, label, test_size=0.30, random_state=69)

    # Create instance of RandomForestClassifier class with chosen training parameters
    forest_classifier = RandomForestClassifier(n_estimators=50, oob_score=True, n_jobs=-1)

    # Build a random forest from the training set of data
    forest_classifier.fit(feature_train, label_train)

    with open ('model_pickle','wb') as model_file:
        pickle.dump(forest_classifier, model_file)
    
    with open("encoder_pickle", "wb") as encoder_file: 
        pickle.dump(feature_encoder, encoder_file)
    