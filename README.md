# ALIM'CONFIANCE - GROUPE 6 - ALLAN, LORRAINE, THIBAUT

### INSTALLATION DES LIBRAIRIES *(voir requirements.txt)*
```
pip install -r requirements.txt
```

### LIBRAIRIES UTILISÉES DANS CE PROJET
```
Flask==2.0.2
Flask_SQLAlchemy==2.5.1
imbalanced_learn==0.9.0
imblearn==0.0
matplotlib==3.5.1
pandas==1.3.5
scikit_learn==1.0.2
SQLAlchemy==1.4.29
tqdm==4.62.3
wget==3.2
```
---
### PREMIER LANCEMENT DE L'APPLICATION
L'application Flask et son serveur web associé s'initie après exécution du fichier **main.py**. *(http://127.0.0.1:5000 par défaut)*

**ATTENTION:** Les étapes suivantes sont **nécessaires** et **obligatoires** si vous souhaitez utiliser la fonction de prédiction.

**STEP 1:** 
Accédez à la page "Panel Admin" via la barre de navigation en haut du site, cliquez sur le bouton "Refresh CSV and Rebase". Attendez qu'un message lisant _"CSV has been refreshed and database has been rebuilt. Good job myself."_ s'affiche en haut de votre navigateur avant de procéder à l'étape suivante. _(cette étape ne devrait pas prendre plus de deux ou trois minutes, les performances de votre ordinateur ont un impact sur la vitesse des diverses opérations.)_

**STEP 2:** 
Toujours depuis la page "Panel Admin", cliquez sur le bouton "Train new classification model". Attendez qu'un message lisant _"Modèle entraîné via régression logistique(grid search), accuracy: x%"_ ou _"Modèle entraîné via random forest(grid search), accuracy: x%"_ s'affiche en haut de votre navigateur avant de procéder vers la page "Home" où se trouve l'outil de prédiction. _(cette étape ne devrait pas prendre plus de vingt minutes et probablement moins que cinq, cette étape va également utiliser 100% de la puissance de votre CPU pour réduire les temps d'opération, merci de ne pas paniquer. les performances de votre ordinateur ont un impact sur la vitesse des diverses opérations.)_

---
### ARCHITECTURE DES TEMPLATES HTML
- base.html -- contient le template principal 
- adminpanel.html -- /admin
- userpanel.html -- /
- proto_back.html -- /proto_back (page prototype non-fonctionnelle laissée à titre historique)

### ARCHITECTURE DES FICHIERS PYTHON
- main.py -- contient la fonction de lancement de l'application et du serveur Flask ainsi que de la création de la base de données
- __init__.py -- contient les paramètres de l'application Flask
- adminpanel.py -- contient la route menant au template adminpanel.html
- userpanel.py -- contient la route menant au template userpanel.html
- proto_back.py -- contient la fonction refresh_and_rebase() _(cf. doc)_
- proto_ml.py -- contient la fonction model_training_module() _(cf. doc)_
- models.py -- contient la structure de la base de données

### FICHIERS QUI SERONT GÉNÉRÉS PENDANT LE PROJET
- __pycache__ -- dossier généré automatiquement après la première transaction avec la base de données
- export_alimconfiance.csv -- fichier .csv, contient les données mise à disposition par Alim'Confiance, généré durant l'éxécution de la fonction refresh_and_rebase() (~7Mb)
- alim_confiance.db -- fichier .db, contient les données extraites du fichier export_alimconfiance.csv, généré durant l'éxécution de la fonction create_database() (~8Mb)
- model_pickle -- fichier binaire brut, contient le modèle de classification entraîné (~163Kb) 
- encoder_pickle -- fichier binaire brut, contient l'encoder (~53kb)
