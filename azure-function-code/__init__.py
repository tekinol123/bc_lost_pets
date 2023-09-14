import logging
import os
import azure.functions as func
from azure.storage.blob import BlobServiceClient
from .scraper import Scraper, duration_to_days
from datetime import datetime
import pytz
import pandas as pd

connection_string = os.environ['STORAGE_ACCOUNT_CONNECTION_STRING']
container_name = os.environ['STORAGE_ACCOUNT_CONTAINER_NAME']
secret_password = os.environ['SECRET_PASSWORD1']

blob_service_client = BlobServiceClient.from_connection_string(connection_string)

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    #Getting raw data from scraper/parser
    if req.headers.get('name')==secret_password:
        pass
    else:
        return func.HttpResponse(
             "Please pass a name on the query string or in the request headers",
             status_code=400
        )
    animals_df = Scraper().parse_animal_data()
    #Data cleasing/transformation
    pst = pytz.timezone('America/Los_Angeles')
    pattern = r"\s*\(\s*approx\s*\)\s*"
    animals_df['age'] = animals_df['age'].replace(pattern, '', regex=True)
    animals_df['age_in_days'] = animals_df['age'].apply(duration_to_days)
    animals_df['date_found']= datetime.now(tz=pst).date()

    current_date = datetime.now(tz=pst).strftime("%Y-%m-%d")
    blob_name = f"{current_date}_animals.csv"

    try:
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        blob_client.upload_blob(animals_df.to_csv(index=False))
        return func.HttpResponse(f"Success! Uploaded {blob_name} to {container_name}")
    except Exception as e:
        return func.HttpResponse(f"Failed to upload {blob_name} to {container_name}: {e}")