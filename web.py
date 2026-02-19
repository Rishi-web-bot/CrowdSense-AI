from flask import Flask, render_template, request, Response, redirect, url_for
import os
import cv2
import time

from src.detection import detect_people
from src.prediction import predict_risk
from src.alarm import check_alarm

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

video_path = None
running = False
people_count_global = 0
status_global = "SAFE"
fps_global = 0


# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")


# ---------------- CROWD PAGE ----------------
@app.route("/crowd", methods=["GET", "POST"])
def crowd():
    global video_path, running

    if request.method == "POST":
        file = request.files["video"]
        video_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(video_path)
        running = True

    return render_template(
        "crowd.html",
        people=people_count_global,
        status=status_global,
        fps=fps_global,
        ai_status="MODEL LOADED ✔",
    )


# ---------------- STOP BUTTON ----------------
@app.route("/stop")
def stop():
    global running
    running = False
    return redirect(url_for("crowd"))


# ---------------- VIDEO STREAM ----------------
def generate_frames():

    global video_path, running
    global people_count_global, status_global, fps_global

    if video_path is None:
        return

    cap = cv2.VideoCapture(video_path)
    frame_index = 0

    while running:
        start = time.time()

        success, frame = cap.read()
        if not success:
            break

        frame_index += 1

        if frame_index % 3 != 0:
            continue

        count, img = detect_people(frame)
        people_count_global = count

        status_global = check_alarm(count)

        if status_global == "HIGH CROWD":
            color = (0, 0, 255)
        elif status_global == "MEDIUM CROWD":
            color = (0, 165, 255)
        else:
            color = (0, 255, 0)

        cv2.putText(
            img,
            f"{status_global} | People:{count}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            color,
            3,
        )

        end = time.time()
        fps_global = round(1 / (end - start), 2)

        ret, buffer = cv2.imencode(".jpg", img)
        frame = buffer.tobytes()

        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")

    cap.release()


@app.route("/video_feed")
def video_feed():
    return Response(
        generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


# ---------------- RISK PAGE (CSV LOOKUP VERSION) ----------------
@app.route("/risk", methods=["GET", "POST"])
def risk():

    risk_level = None
    location_output = None
    temperature_output = None

    if request.method == "POST":

        data = [
            float(request.form["latitude"]),
            float(request.form["longitude"]),
        ]

        result = predict_risk(data)

        location_output = result["location"]
        temperature_output = result["temperature"]
        risk_level = result["risk"]

    return render_template(
        "risk.html",
        result=risk_level,
        location=location_output,
        temperature=temperature_output
    )


if __name__ == "__main__":
    app.run(debug=True)
