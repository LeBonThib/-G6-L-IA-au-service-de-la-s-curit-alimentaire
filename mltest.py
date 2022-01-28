#%%
import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 300
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None
import seaborn as sns
import sklearn
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

test_dataset = 'website/static/downloads/export_alimconfiance.csv'
test_dataframe = pd.read_csv(test_dataset, sep=';')

test_dataframe = test_dataframe.drop(['SIRET','Adresse_2_UA','Numero_inspection','Date_inspection','Agrement','filtre','geores','ods_type_activite','Libelle_commune'], axis = 1)
test_dataframe['Code_postal'].fillna("99000", inplace=True)

X = test_dataframe.loc[:, test_dataframe.columns != 'Synthese_eval_sanit']
y = test_dataframe.loc[:, test_dataframe.columns == 'Synthese_eval_sanit']

from sklearn.preprocessing import OneHotEncoder, LabelEncoder
y['Synthese_eval_sanit'] = LabelEncoder().fit_transform(y['Synthese_eval_sanit'])
ohe = OneHotEncoder()
X = X.astype(str)
X = ohe.fit_transform(X).toarray()

""" 
from imblearn.over_sampling import RandomOverSampler
from collections import Counter
oversampler = RandomOverSampler()
X_resampled, y_resampled = oversampler.fit_resample(X,y)
print(Counter(X))
print(Counter(y))
X_train_resample, X_test_resample, y_train_resample, y_test_resample = model_selection.train_test_split(X_resampled, y_resampled, test_size=0.30, random_state=69) 
"""

from sklearn import model_selection
X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y, test_size=0.30, random_state=69)
y_train = np.ravel(y_train)

from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
classifier = DecisionTreeClassifier(max_leaf_nodes=4)
classifier.fit(X_train, y_train)
y_pred = classifier.predict(X_test)
y_pred.shape
tree.plot_tree(classifier)
bob_test = classifier.score(X_test, y_test)
bob_train = classifier.score(X_train, y_train)
print("Score X_test, y_test:")
print(bob_test)
print("Score X_train, y_train:")
print(bob_train)

from sklearn import metrics
print("Decision Tree Classification Report")
print(metrics.classification_report(y_test, y_pred, zero_division=0))
disp = metrics.plot_confusion_matrix(classifier,X_test, y_test)
disp.figure_.suptitle("Confusion Matrix")
print(f"Confusion matrix:\n{disp.confusion_matrix}")
plt.show();

from sklearn.ensemble import RandomForestClassifier
rfc = RandomForestClassifier(n_estimators=50, oob_score=True, n_jobs=-1)
rfc.fit(X_train, y_train)
y2_pred = rfc.predict(X_test)
print("Random Forest Classification Report")
print(metrics.classification_report(y_test, y2_pred))
disp2 = metrics.plot_confusion_matrix(rfc, X_test, y_test)
disp2.figure_.suptitle("Confusion Matrix")
print(f"Confusion matrix:\n{disp2.confusion_matrix}")
plt.show();
# %%
