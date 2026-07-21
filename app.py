from flask import Flask, render_template, request
import os
import cv2
from ultralytics import YOLO
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "static"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Load trained model
model = YOLO("runs/detect/train/weights/best.pt")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return "No file"

    file = request.files["file"]

    if file.filename == "":
        return "No filename"

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    img = cv2.imread(filepath)

    # GRAYSCALE
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("static/gray.jpg", gray)

    # EDGE DETECTION
    edges = cv2.Canny(gray, 100, 200)
    cv2.imwrite("static/edges.jpg", edges)

    # YOLO DETECTION
    results = model(filepath)
    results[0].save(filename="static/result.jpg")

    # CALCULATE PERCENTAGE
    boxes = results[0].boxes
    names = model.names

    container_height = None
    liquid_height = None

    for box in boxes:
        cls_id = int(box.cls[0])
        label = names[cls_id]

        y1, y2 = box.xyxy[0][1], box.xyxy[0][3]
        height = float(y2 - y1)

        if label == "container":
            container_height = height

        elif label == "liquid":
            liquid_height = height

    if container_height and liquid_height:
        percentage = round((liquid_height / container_height) * 100, 2)
    else:
        percentage = "Not Detected"

    return render_template(
        "index.html",
        original_image=filename,
        gray_image="gray.jpg",
        edge_image="edges.jpg",
        result_image="result.jpg",
        percentage=percentage
    )


if __name__ == "__main__":
    app.run(debug=True)