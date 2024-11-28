# camera.py
# v0.1.0

# Library Used
import cv2
import requests
import yaml
import numpy as np

# Load the configuration from the YAML file
with open('config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

# Open the camera (usually 0 for the default camera)
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    _, img_encoded = cv2.imencode('.jpg', frame)
    detect_response = requests.post(config['endpoint']['equipment_detection'], files={"image": img_encoded.tostring()})
    
    # Convert the JSON response to a Python dictionary
    response_data = detect_response.json()

    # Iterate over each ROI in the response
    for i, roi in enumerate(response_data['roi']):
        x1, y1, x2, y2 = roi
        label = response_data['label'][i]
        score = response_data['identification_score'][i]
        print(label)
        # Color Logic3
        # Determine the color based on the label
        if label in ['NO-Hardhat', 'NO-Mask', 'NO-Safety Vest']:
            color = (0, 0, 255)  # Red for unsafe labels
        else:
            color = (0, 255, 0)  # Green for other labels

        # Draw a rectangle around the ROI
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

        # Create a string to display the label and score
        text = f"{label}: {score:.2f}"

        # Calculate the position for the text
        text_x = x1
        text_y = y1 - 10

        # Draw the text on the image
        cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    cv2.imshow('Face Recognition', frame)

    if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
        break

cap.release()
cv2.destroyAllWindows()