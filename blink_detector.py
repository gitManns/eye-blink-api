import cv2
import mediapipe as mp
import requests
import tempfile
import os

# Download video from URL and save temporarily
def download_video_from_url(video_url):
    response = requests.get(video_url, stream=True)
    if response.status_code != 200:
        raise Exception("Failed to download video")
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                tmp_file.write(chunk)
        return tmp_file.name  # return path to downloaded video

# Blink detection logic
def detect_blinks(video_path):
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False)
    blink_count = 0

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise Exception("Error opening video file")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)

        if results.multi_face_landmarks:
            # Simple placeholder logic — replace with proper EAR or blink condition
            blink_count += 1

    cap.release()
    return blink_count

# Classify health based on blink count
def classify_blink_health(blink_count):
    if blink_count < 5:
        return {
            "blink_status": "Low",
            "recommendation": "Try the 20-20-20 rule. Blink more often to reduce eye strain."
        }
    elif blink_count < 15:
        return {
            "blink_status": "Moderate",
            "recommendation": "Consider taking breaks regularly to keep eyes healthy."
        }
    else:
        return {
            "blink_status": "Healthy",
            "recommendation": "Keep up the good screen habits!"
        }
