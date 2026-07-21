import cv2
import numpy as np
from yolo_segmentation import YOLOSegmentation
# ---------------------------
# Load YOLO model
# ---------------------------
model = YOLOSegmentation("yolov8_segmentation/best.pt")

# ---------------------------
# Open camera (DroidCam index = 1 for you)
# ---------------------------
cap = cv2.VideoCapture(1)
if not cap.isOpened():
    print("❌ Camera not opening")
    exit()

# ---------------------------
# Constants
# ---------------------------
ACTUAL_HEIGHT_OF_FLASK = 291.0  # mm
FLASK_DIAMETER_MM = 38.2        # mm

prev_volume = 0.0
show_saved_text = 0

# ---------------------------
# Helper: pick horizontal line (y) from edges using Hough
# ---------------------------
def get_liquid_line_y(edges):
    lines = cv2.HoughLinesP(
        edges, 1, np.pi/180,
        threshold=60,
        minLineLength=40,
        maxLineGap=10
    )
    if lines is None:
        return None

    ys = []
    for l in lines:
        x1, y1, x2, y2 = l[0]
        if abs(y1 - y2) < 5:  # near-horizontal
            ys.append((y1 + y2) // 2)

    if not ys:
        return None

    # robust estimate
    return int(np.median(ys))


# ---------------------------
# Main loop
# ---------------------------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    img = frame.copy()

    # Per-frame resets
    PIXEL_PER_MM_HEIGHT_RATIO = None
    measured_top_height = 0
    ACTUAL_LIQUID_HEIGHT = 0.0

    # YOLO detection
    bboxes, classes, segs, scores = model.detect(img)

    if classes is not None:
        for bbox, class_id, seg, score in zip(bboxes, classes, segs, scores):
            x, y, x2, y2 = map(int, bbox)

            # 🔴 Flask body → scale (pixels/mm)
            if class_id == 0:
                cv2.rectangle(img, (x, y), (x2, y2), (0, 0, 255), 2)
                measured_flask_height_px = (y2 - y)
                if measured_flask_height_px > 0:
                    PIXEL_PER_MM_HEIGHT_RATIO = measured_flask_height_px / ACTUAL_HEIGHT_OF_FLASK

            # 🔵 Flask top (ellipse height for offset)
            elif class_id == 1:
                measured_top_height = (y2 - y)

            # 🟢 Liquid ROI → apply DIP
            elif class_id == 2:
                cv2.rectangle(img, (x, y), (x2, y2), (0, 255, 0), 2)

                # If we don't yet have a scale, skip refinement this frame
                if PIXEL_PER_MM_HEIGHT_RATIO is None or PIXEL_PER_MM_HEIGHT_RATIO == 0:
                    continue

                # 1) ROI
                roi = img[y:y2, x:x2]

                # 2) Grayscale
                gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

                # 3) Blur
                blur = cv2.GaussianBlur(gray, (5, 5), 0)

                # 4) Threshold (Otsu)
                _, thresh = cv2.threshold(
                    blur, 0, 255,
                    cv2.THRESH_BINARY + cv2.THRESH_OTSU
                )

                # 5) Edge (Canny)
                edges = cv2.Canny(thresh, 50, 150)

                # 6) Horizontal line (liquid surface)
                liquid_y = get_liquid_line_y(edges)

                if liquid_y is not None:
                    # Draw detected surface on full image
                    cv2.line(
                        img,
                        (x, y + liquid_y),
                        (x2, y + liquid_y),
                        (255, 0, 0), 2
                    )

                    # Convert to height (mm)
                    # compensate a bit for top ellipse if available
                    offset_px = measured_top_height / 2 if measured_top_height else 0
                    measured_liquid_height_px = max(0, liquid_y - offset_px)

                    measured_liquid_height_mm = measured_liquid_height_px / PIXEL_PER_MM_HEIGHT_RATIO
                    ACTUAL_LIQUID_HEIGHT = measured_liquid_height_mm

                # (Optional debug windows)
                cv2.imshow("Gray", gray)
                cv2.imshow("Threshold", thresh)
                cv2.imshow("Edges", edges)

    # ---------------------------
    # Volume + Percentage
    # ---------------------------
    current_volume = (np.pi * ((FLASK_DIAMETER_MM / 2) ** 2) * ACTUAL_LIQUID_HEIGHT) / 1000.0 + 22.0

    # smoothing
    MILLILITER = 0.7 * prev_volume + 0.3 * current_volume
    prev_volume = MILLILITER

    percentage = (ACTUAL_LIQUID_HEIGHT / ACTUAL_HEIGHT_OF_FLASK) * 100.0

    # clamp
    MILLILITER = max(0.0, min(500.0, MILLILITER))
    percentage = max(0.0, min(100.0, percentage))

    # ---------------------------
    # Display
    # ---------------------------
    cv2.putText(img, f"Volume: {round(MILLILITER, 2)} ml",
                (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.putText(img, f"Level: {round(percentage, 2)} %",
                (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

    cv2.putText(img, "Press S to Save | ESC to Exit",
                (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # Saved indicator
    if show_saved_text > 0:
        cv2.putText(img, "Saved!", (260, 200),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        show_saved_text -= 1

    cv2.imshow("Liquid Detection (YOLO + DIP)", img)

    # ---------------------------
    # Controls
    # ---------------------------
    key = cv2.waitKey(1) & 0xFF

    if key == ord('s'):
        cv2.imwrite("flask_result.jpg", img)
        print("📸 Image saved successfully!")
        show_saved_text = 30

    if key == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()