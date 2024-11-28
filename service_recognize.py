# service_recognized.py
# v0.2.0

# Library Used
from ultralyticsplus import YOLO, render_result
 # Import numpy
import cv2

# Parameter Used
classy=['Hardhat', 'Mask', 'NO-Hardhat', 'NO-Mask', 'NO-Safety Vest', 'Person', 'Safety Cone', 'Safety Vest', 'machinery', 'vehicle']

# Load the YOLOv8 model

model = YOLO('yolov8s.pt')
model = YOLO('best.pt')

# Set model parameters
model.overrides['conf'] = 0.70  # NMS confidence threshold
model.overrides['iou'] = 0.45  # NMS IoU threshold
model.overrides['agnostic_nms'] = False  # NMS class-agnostic
model.overrides['max_det'] = 1000  # Maximum number of detections per image

def equipment_detection(image):
    raw_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = model.predict(raw_image,verbose=False)
    result = results[0]
    boxes = result.boxes.xyxy
    # # Extracting confidence scores
    scores = result.boxes.conf
    categories = result.boxes.cls
    print(categories)
    boxz = []
    classz = []
    confidz = []
    for i, (x1, y1, x2, y2) in enumerate(boxes):
        # Index Position
        x1 = int(x1.item())
        y1 = int(y1.item())
        x2 = int(x2.item())
        y2 = int(y2.item())
        boxz.append((x1, y1, x2, y2))
        # Get the corresponding class label and confidence score
        categoriez = int(categories[i].item())
        nama_kelas = classy[categoriez]
        classz.append(nama_kelas)
        confidence = float(scores[i].item())
        confidence_asl = confidence*100
        confidz.append(confidence_asl)

    return boxz,classz,confidz