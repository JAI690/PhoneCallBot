from flask import Flask, request, jsonify
from werkzeug.middleware.proxy_fix import ProxyFix
from aws_lambda_wsgi import lambda_handler as handler_adapter
from vonage import Vonage, Auth
from vonage_voice.models import CreateCallRequest, Talk

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

# Vonage Configuration
VONAGE_APPLICATION_ID = '5907ea82-c97c-4d78-bf07-7b5e7c7cad49'
VONAGE_APPLICATION_PRIVATE_KEY = """-----BEGIN PRIVATE KEY-----
... (clave privada aquí) ...
-----END PRIVATE KEY-----"""

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
    return handler_adapter(app, event, context)
