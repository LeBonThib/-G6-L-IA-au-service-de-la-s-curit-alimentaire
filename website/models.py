from asyncio.windows_events import NULL
from modulefinder import STORE_NAME
from website import db

class raw_data(db.Model):
    store_id = db.Column(db.Integer, primary_key=True)
    store_name = db.Column(db.String(5000))
    store_siret = db.Column(db.String(5000))
    store_address = db.Column(db.String(5000))
    store_zipcode = db.Column(db.String(5000))
    store_city = db.Column(db.String(5000))
    store_industry = db.Column(db.String(5000))
    store_approval = db.Column(db.String(5000))
    store_geoloc = db.Column(db.String(5000))
    store_filter = db.Column(db.String(5000))
    store_industry_ods = db.Column(db.String(5000))

class inspection_data(db.Model):
    inspection_id = db.Column(db.String, primary_key=True)
    inspection_date = db.Column(db.String(5000))
    inspection_result = db.Column(db.String(5000))
    store_id = db.Column(db.Integer, db.ForeignKey('raw_data.store_id'), nullable=True)
    prediction_id = db.Column(db.Integer, db.ForeignKey('logs.prediction_id'), nullable=True)

class training_data(db.Model): 
    store_id_training = db.Column(db.Integer, primary_key=True)
    store_name_training = db.Column(db.String(5000))
    store_siret_training = db.Column(db.String(5000))
    store_address_training = db.Column(db.String(5000))
    store_zipcode_training = db.Column(db.String(5000))
    store_city_training = db.Column(db.String(5000))
    store_industry_training = db.Column(db.String(5000))
    store_approval_training = db.Column(db.String(5000))
    store_geoloc_training = db.Column(db.String(5000))
    store_filter_training = db.Column(db.String(5000))
    store_industry_ods_training = db.Column(db.String(5000))

class logs(db.Model):
    prediction_id = db.Column(db.Integer, primary_key=True)
    prediction_log = db.Column(db.String(5000))
    store_id_training = db.Column(db.Integer, db.ForeignKey('training_data.store_id_training'), nullable=True)