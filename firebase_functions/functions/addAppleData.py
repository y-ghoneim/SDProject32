import functions_framework
from firebase_admin import firestore, initialize_app, credentials
from flask import abort, jsonify, request

# Initialize Firebase Admin
initialize_app()

@functions_framework.http
def add_health_data(request):
    # Check for POST request
    if request.method != 'POST':
        return abort(405, description="Method Not Allowed")

    # Get uid from headers
    uid = request.headers.get('uid')
    if not uid:
        return abort(401, description="Unauthorized: No uid provided.")

    try:
        # Initialize Firestore DB
        db = firestore.client()
        user_doc = db.collection('users').document(uid).get()

        if not user_doc.exists:
            return abort(401, description="Unauthorized: uid does not exist.")

        # User exists, now add the health data to 'TestCollection'
        health_data = request.get_json()
        # Add any necessary processing or validation for healthData here
        write_result, _ = db.collection('TestCollection').add(health_data)
        return jsonify(message=f"Patient data added!"), 201

    except Exception as error:
        print(f"Error processing request: {error}")
        return abort(500, description="Internal Server Error")