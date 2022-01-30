#%%
#   IMPORT DES PACKAGES ET LIBS
#
from email.mime import base
from locale import normalize
from xml.etree.ElementInclude import include
import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 300
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
sns.set_style('darkgrid')

#%%
#   OBJECTIF
#
print("- Comprendre la nature des données")
print("- Développer une premiere stratégie de modélisation")

#%%
#   IMPORT DU DATASET
#
base_dataset = 'website/static/downloads/export_alimconfiance.csv'
base_dataframe = pd.read_csv(base_dataset, sep=";")
# base_dataframe = pd.read_tsv(base_dataset)
# base_dataframe = pd.read_excel(base_dataset)
# base_dataframe = pd.read_json(base_dataset)
# base_dataframe = pd.read_sql(base_dataset)

#%%
#   COUP D'OEIL RAPIDE SUR LE DATASET
#
print(f'Informations sur le dataset:')
print(base_dataframe.info())
print(f'Cinq premières lignes du dataset:')
base_dataframe.head()

#%%
#   ANALYSE DE FORME DES DONNEES - PARAMÉTRAGE DE LA TARGET
#
target_label = 'Synthese_eval_sanit'
base_target = base_dataframe[target_label]


#%%
#   CHECKLIST DE BASE
#
print('Analyse de Forme:')
print(f'dimensions:\n{base_dataframe.shape}')
print('types de variables:')
print(f"qualitatives:\n {len(base_dataframe.select_dtypes(include=['object']).columns)}")
print(f"quantitatives:\n {len(base_dataframe.select_dtypes(include=['float','int','uint']).columns)}")

#%%
#   ANALYSE DE FORME DES DONNEES - DTYPES & HEATMAP DES NaN
#
base_dataframe.dtypes.value_counts().plot(kind='pie', title='Répartition des types dans le dataset', label='')
plt.figure().suptitle('Heatmap des cellules vides du dataset')
sns.heatmap(base_dataframe.isna(), cbar=False)

# %%
#   ANALYSE DE FORME DES DONNEES - POURCENTAGE DE NaN PAR COLONNE
#
(base_dataframe.isna().sum()/base_dataframe.shape[0]).sort_values(ascending=False)

# %%
#   ANALYSE DE FOND DES DONNEES - ELIMINATION DES COLONNES INUTILES (>90% NaN)
#
base_dataframe = base_dataframe[base_dataframe.columns[base_dataframe.isna().sum()/base_dataframe.shape[0] <0.9]]

# %%
#   ANALYSE DE FOND DES DONNEES - HEATMAP DES NaN (POST DROP)
#
plt.figure(figsize=(20,10))
sns.heatmap(base_dataframe.isna(), cbar=False)

# %%
#   ANALYSE DE FOND DES DONNEES - EXAMEN DE LA TARGET
#
print(f'Répartition des valeurs dans la cible\n{base_target.value_counts(normalize=True)}')

# %%
#   ANALYSE DE FOND DES DONNEES - DIAGRAMME DE DISTRIBUTION (SI VALEUR NUMÉRIQUE)
#
""" for col in base_dataframe.select_dtypes('float'):
    plt.figure()
    sns.displot(base_dataframe[col]) """

# %%
#   ANALYSE DE FOND DES DONNEES - HISTOGRAMES DES VARIABLES CONTINUES (SI VALEUR NUMÉRIQUE)
#
""" for col in base_dataframe.select_dtypes('float'):
    plt.figure()
    sns.displot(base_dataframe[col]) """

#%%
#   PRÉPARATION À L'ENCODAGE DES FEATURES ET DU LABEL POUR VISUALISATION MATHÉMATIQUE
#
# Assign data from the dataframe to the features and label variables by locating the columns.
features = base_dataframe.loc[:, base_dataframe.columns != target_label]
label = base_target

# Cast features as string to unify type prior to encoding.
features = features.astype(str)

#%%
#   ON ENCODE LE LABEL VIA LABELENCODER ET LES FEATURES VIA ONEHOTENCODER
#
# Import encoders.
from sklearn.preprocessing import OneHotEncoder, LabelEncoder

# Create the encoders.
feature_encoder = OneHotEncoder()
label_encoder = LabelEncoder()

# Apply the encoder.
features = feature_encoder.fit_transform(features)
label = label_encoder.fit_transform(label)

# %%
