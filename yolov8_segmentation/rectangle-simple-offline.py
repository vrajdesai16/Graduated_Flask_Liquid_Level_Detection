import cv2
import numpy as np
from yolo_segmentation import YOLOSegmentation

# Load YOLO model
model = YOLOSegmentation("best.pt")

# ✅ Load image (CHANGE NAME IF NEEDED)
image_path = "graduated-flask/raw-photos1/IMG20230224211106.jpg"
img = cv2.imread(image_path)

# Check if image loaded
if img is None:
    print("❌ Error: Image not found. Check path!")
    exit()

# Resize image
scale_percent = 50
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
img = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)

frame = img.copy()

# Detect objects
bboxes, classes, segmentations, scores = model.detect(frame)

# Constants
ACTUAL_DIAMETER_OF_FLASK = 41.5
ACTUAL_HEIGHT_OF_FLASK = 291

PIXEL_PER_MM_HEIGHT_RATIO = 1
theta = 0
bbox_liquid = [0, 0, 0, 0]
ACTUAL_LIQUID_HEIGHT = 0

if classes is not None:
    for bbox, class_id, seg, score in zip(bboxes, classes, segmentations, scores):
        (x, y, x2, y2) = bbox

        # Flask detection
        if class_id == 0:
            cv2.rectangle(frame, (x, y), (x2, y2), (0, 0, 255), 2)
            measured_flask_height = y2 - y
            PIXEL_PER_MM_HEIGHT_RATIO = measured_flask_height / ACTUAL_HEIGHT_OF_FLASK

        # Flask top (ellipse)
        measured_height = 0
        if class_id == 1:
            cv2.polylines(frame, [seg], True, (255, 0, 0), 2)

            measured_width = x2 - x
            measured_height = y2 - y

            theta = np.arcsin(measured_height / measured_width)

        # Liquid level
        if class_id == 2:
            bbox_liquid = [x, y, x2, y2]
            measured_liquid_height = y2 - y
            if measured_height != 0:
                measured_liquid_height = measured_liquid_height - (measured_height / 2)

            measured_liquid_height_mm = measured_liquid_height / PIXEL_PER_MM_HEIGHT_RATIO
            ACTUAL_LIQUID_HEIGHT = measured_liquid_height_mm / np.cos(theta)

            cv2.rectangle(frame, (x, y), (x2, y2), (0, 255, 0), 2)

# Calculate volume
current_volume = (np.pi * ((38.2/2)**2) * ACTUAL_LIQUID_HEIGHT)/1000 + 22
MILLILITER = (prev_volume + current_volume) / 2
prev_volume = MILLILITER
print("💧 Estimated Volume:", round(MILLILITER, 2), "ml")

# Display result
cv2.putText(frame, f"Volume: {round(MILLILITER,2)} ml",
            (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

cv2.imshow("Result", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
