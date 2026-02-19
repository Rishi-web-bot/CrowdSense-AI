from ultralytics import YOLO
import cv2

model = YOLO("yolov8n.pt")


def detect_people(frame):
    results = model(frame)  # ← UPDATED HERE

    count = 0

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            if cls == 0:
                count += 1

                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cx = int((x1 + x2) / 2)
                cy = int((y1 + y2) / 2)

                if count >= 10:
                    color = (0, 0, 255)
                else:
                    color = (0, 255, 0)

                cv2.circle(frame, (cx, cy), 10, color, -1)

    return count, frame
