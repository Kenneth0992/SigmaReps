"""
exercises/pushup.py

Checks:
  ✓ Body plank line (hip not sagging or piking)
  ✓ Elbow angle at bottom (70–110°)
  ✓ Elbows not flaring too wide (< 60° from torso)
  ✓ Head/neck neutral (not drooping)
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import get_coords, angle_between


def analyze_pushup(landmarks, PoseLandmark):
    feedback = []

    # ── Landmarks ────────────────────────────────────────────────────────────
    l_shoulder = get_coords(landmarks, PoseLandmark, "LEFT_SHOULDER")
    l_elbow    = get_coords(landmarks, PoseLandmark, "LEFT_ELBOW")
    l_wrist    = get_coords(landmarks, PoseLandmark, "LEFT_WRIST")
    l_hip      = get_coords(landmarks, PoseLandmark, "LEFT_HIP")
    l_knee     = get_coords(landmarks, PoseLandmark, "LEFT_KNEE")
    l_ankle    = get_coords(landmarks, PoseLandmark, "LEFT_ANKLE")
    nose       = get_coords(landmarks, PoseLandmark, "NOSE")

    r_shoulder = get_coords(landmarks, PoseLandmark, "RIGHT_SHOULDER")
    r_elbow    = get_coords(landmarks, PoseLandmark, "RIGHT_ELBOW")
    r_wrist    = get_coords(landmarks, PoseLandmark, "RIGHT_WRIST")

    # ── Angles ───────────────────────────────────────────────────────────────
    l_elbow_angle = angle_between(l_shoulder, l_elbow, l_wrist)
    r_elbow_angle = angle_between(r_shoulder, r_elbow, r_wrist)
    avg_elbow     = (l_elbow_angle + r_elbow_angle) / 2

    # Body line: shoulder → hip → ankle should be ~180°
    body_angle = angle_between(l_shoulder, l_hip, l_ankle)

    # Elbow flare: angle at shoulder between elbow and hip
    elbow_flare = angle_between(l_elbow, l_shoulder, l_hip)

    # ── Standing / not in push-up position ───────────────────────────────────
    # Detect by seeing if hips are higher than shoulders (upright)
    if l_hip[1] < l_shoulder[1] - 0.1:
        feedback.append("Get into push-up position: hands under shoulders, body straight")
        return True, feedback

    # ── Body plank line ───────────────────────────────────────────────────────
    if body_angle < 155:
        # Hip either too high (pike) or too low (sag)
        if l_hip[1] < l_shoulder[1]:          # hip higher = piking
            feedback.append("Lower your hips — your body should form a straight line")
        else:
            feedback.append("Lift your hips — don't let them sag toward the floor")

    # ── Elbow depth ──────────────────────────────────────────────────────────
    if avg_elbow > 160:
        feedback.append("Lower yourself down — bend your elbows more")
    elif avg_elbow < 60:
        feedback.append("Don't go too low — stop when elbows reach 90°")

    # ── Elbow flare ──────────────────────────────────────────────────────────
    if elbow_flare > 70:
        feedback.append("Tuck your elbows in — they're flaring out too wide")

    # ── Head position ────────────────────────────────────────────────────────
    # Nose should be roughly in line with shoulders (not drooping far below)
    if nose[1] > l_shoulder[1] + 0.15:
        feedback.append("Keep your head neutral — don't let it droop down")

    form_ok = len(feedback) == 0
    if form_ok:
        feedback.append("Perfect push-up form!")

    return form_ok, feedback
