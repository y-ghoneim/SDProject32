from firebase_functions import https_fn
from firebase_admin import initialize_app

import pandas as pd
from google.cloud import storage
from joblib import load

def classifierPrediction(request):
    # Initialize Google Cloud Storage client
    storage_client = storage.Client()

    # Setup for downloading the CSV file and model
    csv_bucket = storage_client.bucket('source-bucket-name')
    csv_blob = csv_bucket.blob('X_test.csv')
    csv_path = '/tmp/X_test.csv'
    csv_blob.download_to_filename(csv_path)
    
    model_bucket = storage_client.bucket('mlmodels_sd32')
    model_blob = model_bucket.blob('lightgbm_model.joblib')
    model_path = '/tmp/lightgbm_model.joblib'
    model_blob.download_to_filename(model_path)
    model = load(model_path)

    # Load the CSV data and predict
    df = pd.read_csv(csv_path)
    predictions = model.predict(df)

    # Convert predictions to a DataFrame and save as CSV
    predictions_df = pd.DataFrame(predictions, columns=['Prediction'])
    predictions_csv_path = '/tmp/predictions.csv'
    predictions_df.to_csv(predictions_csv_path, index=False)

    # Upload the predictions CSV to a different bucket
    results_bucket = storage_client.bucket('mlmoderesults')  # Specify your results bucket name
    results_blob = results_bucket.blob('predictions.csv')
    results_blob.upload_from_filename(predictions_csv_path)

    return 'Predictions processed and saved successfully.'