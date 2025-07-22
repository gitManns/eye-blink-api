import cv2
import mediapipe as mp

def count_blinks_and_duration(video_path):
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(
        static_image_mode=False,
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )

    cap = cv2.VideoCapture(video_path)

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = 0
    blink_count = 0
    eye_closed = False
    threshold = 0.015

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)

        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0].landmark

            left_ear = abs(landmarks[159].y - landmarks[145].y)
            right_ear = abs(landmarks[386].y - landmarks[374].y)
            avg_ear = (left_ear + right_ear) / 2

            if avg_ear < threshold:
                if not eye_closed:
                    blink_count += 1
                    eye_closed = True
            else:
                eye_closed = False

    cap.release()
    duration_seconds = frame_count / fps if fps > 0 else 0
    return blink_count, duration_seconds
