#%%
#   IMPORT DU MILLION DE PACKAGES ET LIBS
#
import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 300
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None
import sklearn
from sklearn import model_selection
from sklearn import tree
from sklearn import metrics
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from imblearn.over_sampling import RandomOverSampler
from sklearn.ensemble import RandomForestClassifier
from collections import Counter
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

#%%
#   IMPORT DU CSV
#
# Locate and import target dataset into a dataframe
test_dataset = 'website/static/downloads/export_alimconfiance.csv'
test_dataframe = pd.read_csv(test_dataset, sep=';')

#%%
#   ON FAIT SAUTER LES COLONNES DONT ON NE VA PAS SE SERVIR POUR ENTRAINER LE MODÈLE ET ON REMPLIT LES CELLULES VIDES
#
# Remove columns from the dataframe that will not be used to train the model.
test_dataframe = test_dataframe.drop(['SIRET','Adresse_2_UA','Numero_inspection','Date_inspection','Agrement','filtre','geores','ods_type_activite','Libelle_commune'], axis = 1)
# Fill empty cells in targeted column to avoid encoding errors.
test_dataframe['Code_postal'].fillna("99000", inplace=True)

#%%
#   ON ASSIGNE LES COLONNES RESTANTES COMME LABEL ET FEATURES
#
# Assign data from the dataframe to the features and label variables by locating the columns.
features = test_dataframe.loc[:, test_dataframe.columns != 'Synthese_eval_sanit']
label = test_dataframe.loc[:, test_dataframe.columns == 'Synthese_eval_sanit'].values.ravel()

# Cast features as string to unify type prior to encoding.
features = features.astype(str)

#%%
#   ON ENCODE LE LABEL VIA LABELENCODER ET LES FEATURES VIA ONEHOTENCODER
#
# Create the encoders.
feature_encoder = OneHotEncoder()
label_encoder = LabelEncoder()

# Apply the encoder.
features = feature_encoder.fit_transform(features)
label = label_encoder.fit_transform(label)

#%%
#   ON APPLIQUE UN ALGORITHME D'OVERSAMPLING POUR SIMULER DES VALEURS IDENTIQUES À LA CLASSE MINORITAIRE AFIN D'ÉQUILIBRER LE DATASET
#
# Create the sampler.
oversampler = RandomOverSampler()
feature_resampled, label_resampled = oversampler.fit_resample(features,label)

# Compare label classes to check sampling result.
print(f'Label brut:\n{Counter(label)}')
print(f'Label resampled:\n{Counter(label_resampled)}')

#%%
#   ON SPLIT LES VARIABLES LABEL ET FEATURES EN LES SOUS-COMPOSANTES DE TEST ET DE TRAINING (APRÈS RESAMPLING)
#
# Create test and training variables from the oversampled dataframe
feature_train, feature_test, label_train, label_test = model_selection.train_test_split(feature_resampled, label_resampled, test_size=0.30, random_state=69) 

#%%
#   ON PRÉPARE LE CLASSIFIER POUR GÉNERER UN ARBRE DE DECISION
#
# Create instance of DecisionTreeClassifier class with chosen training parameters
tree_classifier = DecisionTreeClassifier(max_leaf_nodes=4, max_depth=10)

# Build a decision tree from the training set of data
tree_classifier.fit(feature_train, label_train)

# Predict a class for each feature
tree_label_pred = tree_classifier.predict(feature_test)

#%%
#   ON AFFICHE L'ARBRE DE DÉCISION
#
# Display decision tree 
tree.plot_tree(tree_classifier);

#%%
#   ON EXTRAIT LES SCORES DU MODELE (DECISION TREE)
#
# Add return of score function to variable for further exploitation of data
test_tree_score = tree_classifier.score(feature_test, label_test)
train_tree_score = tree_classifier.score(feature_train, label_train)

# Compare training and test scores
print(f'Score feature_test, label_test:\n{test_tree_score}')
print(f'Score feature_train, label_train:\n{train_tree_score}')

# %%
#   ON AFFICHE LA MATRICE DE CONFUSION (DECISION TREE)
#
# Display classification report of Decision Tree
print("Decision Tree Classification Report")
print(metrics.classification_report(label_test, tree_label_pred, zero_division=0))

# Display confusion matrix
tree_matrix = metrics.plot_confusion_matrix(tree_classifier, feature_test, label_test)
tree_matrix.figure_.suptitle("Confusion Matrix (Decision Tree)")
print(f"Confusion matrix:\n{tree_matrix.confusion_matrix}")
plt.show();

# %%
#   ON PRÉPARE LE CLASSIFIER POUR GÉNERER UNE RANDOM FOREST
#
# Create instance of RandomForestClassifier class with chosen training parameters
forest_classifier = RandomForestClassifier(n_estimators=50, oob_score=True, n_jobs=-1)

# Build a random forest from the training set of data
forest_classifier.fit(feature_train, label_train)

# Predict a class for each feature
forest_label_pred = forest_classifier.predict(feature_test)

# %%
#   ON EXTRAIT LES SCORES DU MODELE (RANDOM FOREST)
#
# Display classification report of Random Forest
print("Random Forest Classification Report")
print(metrics.classification_report(label_test, forest_label_pred, zero_division=0))

# %%
#   ON AFFICHE LA MATRICE DE CONFUSION (RANDOM FOREST)
#
# Display confusion matrix
forest_matrix = metrics.plot_confusion_matrix(forest_classifier, feature_test, label_test)
forest_matrix.figure_.suptitle("Confusion Matrix (Random Forest)")
print(f"Confusion matrix:\n{forest_matrix.confusion_matrix}")
plt.show();