import cv2
cap = cv2.VideoCapture(1)
prev_volume=0

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # 👉 your YOLO detection code here
    # (drawing boxes, calculating volume, etc.)

    cv2.imshow("Result", frame)

    key = cv2.waitKey(1)   # 👈 THIS LINE IS IMPORTANT

    # ✅ ADD YOUR CODE HERE 👇
    if key == ord('s'):
        cv2.imwrite("result.jpg", frame)
        print("📸 Result saved")

    if key == 27:  # ESC key
        break

cap.release()
cv2.destroyAllWindows()