import pandas as pd
import wget
import os

from flask import Blueprint, render_template, request, flash
from website import db
from .models import raw_data, inspection_data
from tqdm import tqdm

proto_back = Blueprint('proto_back', __name__)

@proto_back.route('/proto_back', methods=['GET','POST'])
def proto_back_panel():
    if request.method == 'POST':
        refresh_and_rebase()
    return render_template("proto_back.html")

def refresh_and_rebase():
    imported_csv = 'website/static/downloads/export_alimconfiance.csv'
    download_location_folder = 'website/static/downloads'
    if os.path.exists(imported_csv):
        os.remove(imported_csv)
    db.session.query(raw_data).delete()
    db.session.query(inspection_data).delete()
    db.session.commit()

    download_location_url = 'https://dgal.opendatasoft.com/explore/dataset/export_alimconfiance/download/?format=csv&timezone=Europe/Berlin&lang=en&use_labels_for_header=true&csv_separator=%3B'
    wget.download(download_location_url, download_location_folder)

    alimconfiance_dataset_raw = pd.read_csv(imported_csv, sep=';')
    alimconfiance_dataset_raw.fillna("_", inplace=True)

    print(alimconfiance_dataset_raw.info())

    loop_length = len(alimconfiance_dataset_raw)
    separator = "|"

    for r in tqdm(range(0, loop_length)):
        row = alimconfiance_dataset_raw.iloc[r]
        
        store_name = row["APP_Libelle_etablissement"]
        store_siret = row["SIRET"]
        store_address = row["Adresse_2_UA"]
        store_zipcode = row["Code_postal"] 
        store_city = row["Libelle_commune"]
        store_industry = row["APP_Libelle_activite_etablissement"]
        store_approval = row["Agrement"]
        store_geoloc = row["geores"] 
        store_filter = row["filtre"] 
        store_industry_ods = row["ods_type_activite"] 
        
        inspection_id = row["Numero_inspection"]
        inspection_date = row["Date_inspection"] 
        inspection_result = row["Synthese_eval_sanit"]

        industries = store_industry.split(separator)
        approvals = str(store_approval).split(separator)
        for industry in industries:
            for approval in approvals:
                new_raw_row = raw_data(
                    store_name=store_name, 
                    store_siret=store_siret, 
                    store_address=store_address, 
                    store_zipcode=store_zipcode, 
                    store_city=store_city,
                    store_industry=industry, #
                    store_approval=approval, #
                    store_geoloc=store_geoloc, 
                    store_filter=store_filter, 
                    store_industry_ods=store_industry_ods
                )
                db.session.add(new_raw_row)
                store_id_query = raw_data.query.filter_by(store_id=r+1).first()
                store_id = store_id_query.store_id
                new_inspection_row = inspection_data(
                inspection_id=inspection_id,
                inspection_date=inspection_date,
                inspection_result=inspection_result,
                store_id=store_id
                )
                db.session.add(new_inspection_row)
            # print(r)
    db.session.commit()
    flash("CSV has been refreshed and database has been rebuilt. Good job myself.", category='success')
    return render_template("adminpanel.html")