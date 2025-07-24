import cv2
import mediapipe as mp
import requests
import tempfile
import numpy as np
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
    
def eye_aspect_ratio(upper_point, lower_point):
    return np.linalg.norm(upper_point - lower_point)


# Blink detection logic
def detect_blinks(video_path):
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False)
    blink_count = 0
    blinked = False

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise Exception("Could not open video.")

    while True:
        success, frame = cap.read()
        if not success:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # Get landmark coordinates
                landmarks = face_landmarks.landmark

                # Get left eye points (e.g. 159 and 145)
                top_lid = np.array([landmarks[159].x, landmarks[159].y])
                bottom_lid = np.array([landmarks[145].x, landmarks[145].y])
                ear = eye_aspect_ratio(top_lid, bottom_lid)
                #print(f"EAR: {ear:.5f}")
                # Threshold for blink (tweak based on testing)
                if ear < 0.014 and not blinked:
                    blink_count += 1
                    blinked = True
                elif ear > 0.019:
                    blinked = False

    cap.release()
    return blink_count

# Classify health based on blink count
def classify_blink_health(blink_count):
    if blink_count < 3:
        return {
            "blink_status": "Low",
            "recommendation": "Try the 20-20-20 rule. Blink more often to reduce eye strain. You may have Myopia, please consult an Eye Specialist"
        }
    elif blink_count < 5:
        return {
            "blink_status": "Moderate",
            "recommendation": "Consider taking breaks regularly to keep eyes healthy."
        }
    else:
        return {
            "blink_status": "Healthy",
            "recommendation": "Keep up the good screen habits!"
        }
