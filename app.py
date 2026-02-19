import cv2

# Import modules
from src.detection import detect_people
from src.alarm import check_alarm
from src.prediction import predict_risk
from config.paths import VIDEO1

# 🎥 Load dataset video instead of webcam
cap = cv2.VideoCapture(str(VIDEO1))

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # ----------------------------
    # 1️⃣ Detect People
    # ----------------------------
    count, img = detect_people(frame)

    # ----------------------------
    # 2️⃣ Alarm Check
    # ----------------------------
    alarm_status = check_alarm(count)

    # ----------------------------
    # 3️⃣ Risk Prediction
    # (example parameters)
    # ----------------------------
    latitude = 21.4225
    longitude = 39.8262
    temperature = 40
    time = 14
    location = 0  # encoded value (MasjidAlHaram)

    risk = predict_risk([latitude, longitude, temperature, time, location, count])

    # ----------------------------
    # 4️⃣ Color based on risk
    # ----------------------------
    if risk == "High":
        color = (0,0,255)   # 🔴 RED
    elif risk == "Medium":
        color = (0,165,255) # 🟠 ORANGE
    else:
        color = (0,255,0)   # 🟢 GREEN

    # ----------------------------
    # 5️⃣ Display Output
    # ----------------------------
    cv2.putText(img, f"People: {count}",
                (20,40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,color,2)

    cv2.putText(img, f"Risk: {risk}",
                (20,80),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,color,2)

    cv2.putText(img, f"Alarm: {alarm_status}",
                (20,120),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,color,2)

    cv2.imshow("CrowdSense V2", img)

    # ESC to exit
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()

