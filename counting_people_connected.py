
import cv2
import threading
import time
from flask import Flask, Response, jsonify, render_template_string
from ultralytics import YOLO

app = Flask(__name__)
model = YOLO("yolov8n.pt")

cap = cv2.VideoCapture(0)
lock = threading.Lock()

total_passed = 0
live_count = 0
previous_side = {}
counted_ids = set()
latest_frame = None

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>People Counter Dashboard</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { box-sizing: border-box; }
        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: #0b1120;
            color: white;
            text-align: center;
        }
        header { padding: 24px 12px; }
        header h1 { margin-bottom: 8px; }
        header p { color: #aab7d0; }
        .cards {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 18px;
            padding: 10px 20px 25px;
        }
        .card {
            background: #172238;
            border: 1px solid #2c3b57;
            border-radius: 16px;
            padding: 22px;
            width: 230px;
        }
        .card p { color: #aab7d0; margin: 0; }
        .number { font-size: 48px; font-weight: bold; margin-top: 14px; }
        .green { color: #4ade80; }
        .blue { color: #60a5fa; }
        .video {
            width: 90%;
            max-width: 850px;
            border: 2px solid #334563;
            border-radius: 14px;
        }
        .status { color: #4ade80; margin: 18px; }
        footer { color: #8b9ab5; padding: 20px; }
    </style>
</head>
<body>
    <header>
        <h1>People Counter</h1>
        <p>Real-time people tracking dashboard</p>
    </header>

    <div class="cards">
        <div class="card">
            <p>Total People Passed</p>
            <div class="number green" id="total">0</div>
        </div>
        <div class="card">
            <p>People Currently Visible</p>
            <div class="number blue" id="live">0</div>
        </div>
    </div>

    <h3>Live Camera Feed</h3>
    <img class="video" src="/video_feed" alt="Camera feed">
    <div class="status" id="status">Connecting to camera...</div>

    <footer>Powered by Python, Flask, OpenCV and YOLO</footer>

    <script>
        async function updateCounts() {
            try {
                const response = await fetch('/counts');
                const data = await response.json();
                document.getElementById('total').textContent = data.total;
                document.getElementById('live').textContent = data.live;
                document.getElementById('status').textContent =
                    '● Camera connected | Live updates active';
            } catch (error) {
                document.getElementById('status').textContent =
                    'Waiting for camera/server...';
            }
        }
        updateCounts();
        setInterval(updateCounts, 500);
    </script>
</body>
</html>
"""


def generate_frames():
    global total_passed, live_count, latest_frame

    while True:
        success, frame = cap.read()

        if not success:
            time.sleep(0.1)
            continue

        height, width = frame.shape[:2]
        line_x = width // 2

        results = model.track(
            frame,
            persist=True,
            tracker="bytetrack.yaml",
            classes=[0],
            conf=0.35,
            verbose=False
        )

        current_live = 0

        for result in results:
            if result.boxes is None or result.boxes.id is None:
                continue

            boxes = result.boxes
            ids = boxes.id.int().cpu().tolist()

            for box, track_id in zip(boxes, ids):
                current_live += 1

                x1, y1, x2, y2 = map(
                    int, box.xyxy[0].tolist()
                )

                center_x = (x1 + x2) // 2
                center_y = (y1 + y2) // 2

                side = 1 if center_x >= line_x else 0

                if track_id in previous_side:
                    old_side = previous_side[track_id]

                # Left to Right: Increase count
                    if old_side == 0 and side == 1:
                      total_passed += 1

                    # Right to Left: Decrease count
                    elif old_side == 1 and side == 0:
                        total_passed = max(0, total_passed - 1)

                previous_side[track_id] = side

                cv2.rectangle(
                    frame, (x1, y1), (x2, y2),
                    (0, 255, 0), 2
                )
                cv2.putText(
                    frame, f"ID: {track_id}",
                    (x1, max(y1 - 10, 20)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6, (0, 255, 0), 2
                )

        live_count = current_live

        # Vertical counting line
        cv2.line(
            frame, (line_x, 0), (line_x, height),
            (0, 0, 255), 3
        )

        cv2.putText(
            frame, f"Total Passed: {total_passed}",
            (20, 40), cv2.FONT_HERSHEY_SIMPLEX,
            0.8, (0, 255, 255), 2
        )

        # Save the latest annotated frame
        with lock:
            latest_frame = frame.copy()

        ok, buffer = cv2.imencode(".jpg", frame)

        if not ok:
            continue

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n"
            + buffer.tobytes() + b"\r\n"
        )


@app.route("/")
def home():
    return render_template_string(HTML)


@app.route("/video_feed")
def video_feed():
    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/counts")
def counts():
    return jsonify({
        "total": total_passed,
        "live": live_count
    })


if __name__ == "__main__":
    if not cap.isOpened():
        print("Camera could not be opened. Check your webcam.")
    else:
        print("Website starting...")
        print("People counter API: http://127.0.0.1:5001/counts")
        app.run(host="127.0.0.1", port=5001, threaded=True)

    cap.release()