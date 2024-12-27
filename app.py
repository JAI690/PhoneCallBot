from flask import Flask, request, jsonify
from werkzeug.middleware.proxy_fix import ProxyFix
import aws_lambda_wsgi
from vonage import Vonage, Auth
from vonage_voice.models import CreateCallRequest, Talk
import boto3
import json

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

# Configuración global para secretos
def get_secret(secret_name):
    """Retrieve secret from AWS Secrets Manager."""
    client = boto3.client('secretsmanager', region_name='us-east-1')
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        secret = get_secret_value_response['SecretString']
        return json.loads(secret)
    except Exception as e:
        print(f"Error retrieving secret: {e}")
        return None

# Obtener los secretos al iniciar la aplicación
secrets = get_secret('flask-api-secrets')
VONAGE_APPLICATION_ID = secrets.get('VONAGE_APPLICATION_ID') if secrets else None
VONAGE_APPLICATION_PRIVATE_KEY = secrets.get('VONAGE_APPLICATION_PRIVATE_KEY') if secrets else None
VONAGE_APPLICATION_PRIVATE_KEY = VONAGE_APPLICATION_PRIVATE_KEY.replace("«", "\r\n")

@app.route('/call', methods=['POST'])
def call():
    data = request.json
    phone_number = data.get('phone_number')

    if not phone_number:
        return jsonify({"error": "Phone number is required."}), 400

    try:

        # Create an Auth instance
        auth = Auth(application_id=VONAGE_APPLICATION_ID, private_key=VONAGE_APPLICATION_PRIVATE_KEY)
        # Create a Vonage instance
        vonage_client = Vonage(auth=auth)
        
        ncco = [Talk(text='Hello world', loop=3, language='en-GB')]

        call = CreateCallRequest(
            to=[{'type': 'phone', 'number': phone_number}],
            ncco=ncco,
            random_from_number=True,
        )

        response = vonage_client.voice.create_call(call)
        print(response.model_dump())

        # Save initial state to DynamoDB

        return jsonify({"message": "Call initiated.", "call_sid": response.model_dump()}), 200
    except Exception as e:
        return jsonify({"error": str(e), "request": request.data}), 500

@app.route('/getCall', methods=['GET'])
def get_call():
    data = request.json
    call_sid = data.get('call_sid')

    if not call_sid:
        return jsonify({"error": "Call SID is required."}), 400

    try:
         # Create an Auth instance
        auth = Auth(application_id=VONAGE_APPLICATION_ID, private_key=VONAGE_APPLICATION_PRIVATE_KEY)
        # Create a Vonage instance
        vonage_client = Vonage(auth=auth)

        call = vonage_client.voice.get_call(call_sid)


        return jsonify({"message": "Status updated.", "status": call.model_dump()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500 

# Lambda handler
def lambda_handler(event, context):
    return aws_lambda_wsgi.response(app, event, context)
