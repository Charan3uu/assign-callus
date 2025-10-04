import cv2
import mediapipe as mp
import numpy as np
import json
from collections import Counter

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

POSES = {
    "T_pose": lambda lm: abs(lm[mp_pose.PoseLandmark.LEFT_WRIST.value].y -
                              lm[mp_pose.PoseLandmark.RIGHT_WRIST.value].y) < 0.05 and
                         lm[mp_pose.PoseLandmark.LEFT_ELBOW.value].y < lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y,
    
    "Hands_Up": lambda lm: lm[mp_pose.PoseLandmark.LEFT_WRIST.value].y < lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y and
                           lm[mp_pose.PoseLandmark.RIGHT_WRIST.value].y < lm[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y,
    
    "Arms_Down": lambda lm: lm[mp_pose.PoseLandmark.LEFT_WRIST.value].y > lm[mp_pose.PoseLandmark.LEFT_HIP.value].y and
                            lm[mp_pose.PoseLandmark.RIGHT_WRIST.value].y > lm[mp_pose.PoseLandmark.RIGHT_HIP.value].y
}

def detect_dance_poses(video_path, output_json="dance_summary.json"):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Cannot open video {video_path}")

    pose_counter = Counter()
    frame_count = 0

    with mp_pose.Pose(min_detection_confidence=0.5,
                      min_tracking_confidence=0.5) as pose:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame_count += 1
            img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(img_rgb)

            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark
                for pose_name, check_fn in POSES.items():
                    if check_fn(landmarks):
                        pose_counter[pose_name] += 1

    cap.release()

    summary = {
        "total_frames": frame_count,
        "pose_counts": dict(pose_counter)
    }

    with open(output_json, "w") as f:
        json.dump(summary, f, indent=4)

    return summary


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True, help="E:\pose\pose_analyser\sample2.mp4")
    parser.add_argument("--out", default="summary.json", help="Output JSON file")
    args = parser.parse_args()

    summary = detect_dance_poses(args.video, args.out)
    print("Dance summary saved to", args.out)
    print(summary)
