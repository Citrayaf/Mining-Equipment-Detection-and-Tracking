# controller.py
# v0.1.0

# Library used
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from flask_sslify import SSLify
import cv2
import numpy as np
from service_recognize import equipment_detection
import logging

app = Flask(__name__)
CORS(app)
sslify = SSLify(app)

logging.basicConfig(filename='app.log', level=logging.DEBUG)

# API Service to Identify Equipment
@app.route('/equipment_detector', methods=['POST'])
def equipment_detector():

    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}),403

    image = request.files['image'].read()
    image = cv2.imdecode(np.frombuffer(image, np.uint8), cv2.IMREAD_COLOR)

    boxes, labels, scores = equipment_detection(image)
    image_height, image_width, _ = image.shape


    return jsonify({'roi':boxes,'label':labels,'identification_score':scores, 'image_width': image_width, 'image_height': image_height})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5014,debug=True, ssl_context=('cert.pem', 'key.pem'))
    #app.run(host='0.0.0.0', port=5014,debug=True)
