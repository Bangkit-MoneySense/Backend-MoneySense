import os
import numpy as np
from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from PIL import Image
from google.cloud import firestore
import uuid
from datetime import datetime

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "config/service-account.json"  
db = firestore.Client()

app = Flask(__name__)

model = load_model('MoneyDetector.h5')
VALID_API_KEY = "12345"

predictions_ref = db.collection('predictions')

def process_image(image):
    try:
        image = image.convert('RGB')  
        image = image.resize((120, 120))  
        image_array = np.array(image, dtype=np.float32) / 255.0  
        image_array = np.expand_dims(image_array, axis=0)  
        return image_array
    except Exception as e:
        raise ValueError(f"Error during image processing: {e}")

def check_api_key():
    api_key = request.headers.get('apikey')
    if api_key != VALID_API_KEY:
        return jsonify({'status': 'fail', 'message': 'Invalid API key.'}), 403
    return None  

@app.route('/predict', methods=['POST'])
def predict():
    api_check_response = check_api_key()
    if api_check_response:
        return api_check_response

    try:
        file = request.files.get('input')
        user_id = request.form.get('userId')

        if not file or not user_id:
            return jsonify({
                'status': 'fail',
                'message': 'Both image and userId are required.'
            }), 400

        image = Image.open(file.stream)
        input_data = process_image(image)
        authenticity_pred, nominal_pred = model.predict(input_data)

        authenticity = "Asli" if authenticity_pred[0][0] > 0.5 else "Palsu"
        authenticity_confidence = float(authenticity_pred[0][0])

        nominal_index = int(np.argmax(nominal_pred[0]))
        nominal_confidence = float(np.max(nominal_pred[0]))

        nominal_map = {
            0: "Rp1.000",
            1: "Rp2.000",
            2: "Rp5.000",
            3: "Rp10.000",
            4: "Rp20.000",
            5: "Rp50.000",
            6: "Rp100.000",
        }
        nominal = nominal_map.get(nominal_index, "Nominal tidak dikenali")

        prediction_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()

        prediction_data = {
            'userId': user_id,
            'currency': nominal,
            'authenticity': authenticity,
            'nominal_confidence': nominal_confidence,
            'authenticity_confidence': authenticity_confidence,
            'createdAt': timestamp
        }

        predictions_ref.document(prediction_id).set(prediction_data)

        return jsonify({
            'status': 'success',
            'data': {
                'id': prediction_id,
                'userId': user_id,
                'currency': nominal,
                'authenticity': authenticity,
                'authenticity_confidence': round(authenticity_confidence, 2),
                'nominal_confidence': round(nominal_confidence, 2),
                'createdAt': timestamp
            }
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/history', methods=['GET'])
def get_history():
    api_check_response = check_api_key()
    if api_check_response:
        return api_check_response

    try:
        user_id = request.args.get('userId')

        if not user_id:
            return jsonify({
                'status': 'fail',
                'message': 'userId is required.'
            }), 400

        user_predictions = predictions_ref.where('userId', '==', user_id).stream()

        records = []
        for doc in user_predictions:
            record = doc.to_dict()
            records.append({
                'id': doc.id,
                'userId': record['userId'],
                'currency': record['currency'],
                'authenticity': record['authenticity'],
                'nominal_confidence': record['nominal_confidence'],
                'authenticity_confidence': record['authenticity_confidence'],
                'createdAt': record['createdAt']
            })

        return jsonify({
            'status': 'success',
            'data': records
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
@app.route('/index')
def index():
    return jsonify({'message': 'Aplikasi deteksi uang berjalan..'})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8000)
