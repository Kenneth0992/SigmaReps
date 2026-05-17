"""
FormCheck - AI Bodyweight Exercise Form Analyzer
Run this file to start the program: python main.py
"""

import cv2
import mediapipe as mp
import numpy as np
from exercises.squat import analyze_squat
from exercises.pushup import analyze_pushup
from exercises.lunge import analyze_lunge
from exercises.plank import analyze_plank
from ui.overlay import draw_overlay, draw_menu

# ── Available exercises ──────────────────────────────────────────────────────
EXERCISES = {
    "1": ("Squat",   analyze_squat),
    "2": ("Push-Up", analyze_pushup),
    "3": ("Lunge",   analyze_lunge),
    "4": ("Plank",   analyze_plank),
}

def main():
    mp_pose     = mp.solutions.pose
    mp_drawing  = mp.solutions.drawing_utils
    mp_styles   = mp.solutions.drawing_styles

    cap = cv2.VideoCapture(0)          # 0 = default webcam
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,  1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    current_exercise_name     = None
    current_analyzer          = None
    show_menu                 = True

    print("\n=== FormCheck — Bodyweight Edition ===")
    print("Press 1-4 to pick an exercise | M = menu | Q = quit\n")

    with mp_pose.Pose(
        min_detection_confidence=0.6,
        min_tracking_confidence=0.6,
        model_complexity=1,
    ) as pose:

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Camera not found. Check your webcam connection.")
                break

            frame = cv2.flip(frame, 1)           # mirror so it feels natural
            rgb   = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            rgb.flags.writeable = False
            results = pose.process(rgb)
            rgb.flags.writeable = True

            feedback   = []
            form_ok    = False

            if results.pose_landmarks:
                # Draw skeleton
                mp_drawing.draw_landmarks(
                    frame,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp_styles.get_default_pose_landmarks_style(),
                )

                # Run selected exercise analyzer
                if current_analyzer:
                    landmarks = results.pose_landmarks.landmark
                    form_ok, feedback = current_analyzer(landmarks, mp_pose.PoseLandmark)

            # Draw UI overlay
            draw_overlay(frame, current_exercise_name, form_ok, feedback)
            if show_menu:
                draw_menu(frame, EXERCISES)

            cv2.imshow("FormCheck", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
            elif key == ord("m"):
                show_menu = not show_menu
            elif chr(key) in EXERCISES:
                name, analyzer          = EXERCISES[chr(key)]
                current_exercise_name   = name
                current_analyzer        = analyzer
                show_menu               = False
                print(f"[FormCheck] Exercise: {name}")

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
