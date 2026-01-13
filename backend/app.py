from flask import Flask, request, jsonify
from flask_cors import CORS
import os

from yolo_runner import run_yolo
from traffic_logic import optimize_traffic

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = os.path.abspath("uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/analyze", methods=["POST"])
def analyze_video():
    if "video" not in request.files:
        return jsonify({"error": "No video uploaded"}), 400

    video = request.files["video"]
    input_path = os.path.join(UPLOAD_FOLDER, video.filename)
    video.save(input_path)

    try:
        # Run YOLO — logs go to terminal directly
        vehicle_counts, _ = run_yolo(input_path, video.filename)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Run traffic optimization
    signal_timings = optimize_traffic(vehicle_counts)

    # Return only results, no video
    return jsonify({
        "vehicle_counts": vehicle_counts,
        "signal_timings": signal_timings
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
