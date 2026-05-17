"""
exercises/plank.py

Checks:
  ✓ Body alignment: shoulder → hip → ankle ~180° (no sag/pike)
  ✓ Hips not too high (piking)
  ✓ Hips not too low (sagging)
  ✓ Head neutral (ears in line with shoulders)
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import get_coords, angle_between


def analyze_plank(landmarks, PoseLandmark):
    feedback = []

    # ── Landmarks ────────────────────────────────────────────────────────────
    l_shoulder = get_coords(landmarks, PoseLandmark, "LEFT_SHOULDER")
    l_hip      = get_coords(landmarks, PoseLandmark, "LEFT_HIP")
    l_ankle    = get_coords(landmarks, PoseLandmark, "LEFT_ANKLE")
    l_knee     = get_coords(landmarks, PoseLandmark, "LEFT_KNEE")
    nose       = get_coords(landmarks, PoseLandmark, "NOSE")
    l_ear      = get_coords(landmarks, PoseLandmark, "LEFT_EAR")

    r_shoulder = get_coords(landmarks, PoseLandmark, "RIGHT_SHOULDER")
    r_hip      = get_coords(landmarks, PoseLandmark, "RIGHT_HIP")

    # ── Detect plank position ─────────────────────────────────────────────────
    # In a plank, hips should be roughly at same level or slightly above shoulders
    # If person is standing, skip
    hip_shoulder_diff = abs(l_hip[1] - l_shoulder[1])
    if hip_shoulder_diff < 0.05:           # very small diff = upright (standing)
        feedback.append("Get into plank position: hands under shoulders, body straight")
        return True, feedback

    # ── Body line check ──────────────────────────────────────────────────────
    body_angle = angle_between(l_shoulder, l_hip, l_ankle)

    if body_angle < 160:
        # Determine if sag or pike based on hip y position
        if l_hip[1] > l_shoulder[1] + 0.05:     # hip lower = sagging
            feedback.append("Lift your hips — they're drooping toward the floor")
        elif l_hip[1] < l_shoulder[1] - 0.05:   # hip higher = piking
            feedback.append("Lower your hips — your bum is too high in the air")

    # ── Knee check (should be straight in full plank) ─────────────────────────
    knee_angle = angle_between(l_hip, l_knee, l_ankle)
    if knee_angle < 160:
        feedback.append("Straighten your legs — don't bend at the knees")

    # ── Head / neck neutral ──────────────────────────────────────────────────
    # Ear should be close to shoulder y-level (within a threshold)
    ear_shoulder_diff = l_ear[1] - l_shoulder[1]
    if ear_shoulder_diff > 0.12:
        feedback.append("Head too low — look slightly ahead to keep neck neutral")
    elif ear_shoulder_diff < -0.12:
        feedback.append("Head too high — tuck your chin slightly to align your neck")

    form_ok = len(feedback) == 0
    if form_ok:
        feedback.append("Solid plank — keep breathing and hold strong!")

    return form_ok, feedback
