from flask import Flask, request, jsonify
from app import detect_dance_poses
import os
import tempfile

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze_video():
    if 'video' not in request.files:
        return jsonify({"error": "No video file uploaded"}), 400
    
    video_file = request.files['video']
    temp_dir = tempfile.mkdtemp()
    video_path = os.path.join(temp_dir, video_file.filename)
    video_file.save(video_path)

    try:
        summary = detect_dance_poses(video_path)
        return jsonify(summary)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        os.remove(video_path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
