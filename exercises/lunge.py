"""
exercises/lunge.py

Checks:
  ✓ Front knee angle 80–100° at bottom
  ✓ Front knee not past toes (x-axis check)
  ✓ Back knee close to floor (not too high)
  ✓ Torso upright (not leaning forward)
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import get_coords, angle_between


def _detect_front_leg(landmarks, PoseLandmark):
    """Return landmarks for front and back legs based on who is forward."""
    l_ankle = get_coords(landmarks, PoseLandmark, "LEFT_ANKLE")
    r_ankle = get_coords(landmarks, PoseLandmark, "RIGHT_ANKLE")
    # Lower y = higher in image (further back in a forward lunge from side view)
    # We use x for left/right separation; assume camera is front-facing
    # Front leg = whichever knee has more bend (lower angle)
    l_hip   = get_coords(landmarks, PoseLandmark, "LEFT_HIP")
    l_knee  = get_coords(landmarks, PoseLandmark, "LEFT_KNEE")
    r_hip   = get_coords(landmarks, PoseLandmark, "RIGHT_HIP")
    r_knee  = get_coords(landmarks, PoseLandmark, "RIGHT_KNEE")

    l_angle = angle_between(l_hip, l_knee, l_ankle)
    r_angle = angle_between(r_hip, r_knee, r_ankle)

    if l_angle < r_angle:
        return "LEFT", "RIGHT"
    return "RIGHT", "LEFT"


def analyze_lunge(landmarks, PoseLandmark):
    feedback = []

    front, back = _detect_front_leg(landmarks, PoseLandmark)

    f_hip    = get_coords(landmarks, PoseLandmark, f"{front}_HIP")
    f_knee   = get_coords(landmarks, PoseLandmark, f"{front}_KNEE")
    f_ankle  = get_coords(landmarks, PoseLandmark, f"{front}_ANKLE")
    f_foot   = get_coords(landmarks, PoseLandmark, f"{front}_FOOT_INDEX")

    b_hip    = get_coords(landmarks, PoseLandmark, f"{back}_HIP")
    b_knee   = get_coords(landmarks, PoseLandmark, f"{back}_KNEE")
    b_ankle  = get_coords(landmarks, PoseLandmark, f"{back}_ANKLE")

    shoulder = get_coords(landmarks, PoseLandmark, f"{front}_SHOULDER")

    # Angles
    front_knee_angle = angle_between(f_hip, f_knee, f_ankle)
    torso_angle      = angle_between(shoulder, f_hip, f_knee)

    # ── Standing / neutral ────────────────────────────────────────────────────
    if front_knee_angle > 160:
        feedback.append("Step forward into a lunge — one large step forward")
        return True, feedback

    # ── Front knee depth ─────────────────────────────────────────────────────
    if front_knee_angle > 110:
        feedback.append("Lunge deeper — lower your back knee toward the floor")
    elif front_knee_angle < 70:
        feedback.append("Too deep — come up slightly on your front knee")

    # ── Front knee over toes ─────────────────────────────────────────────────
    # Knee x should not be ahead of foot index x (front view: both same x roughly)
    # In front-facing camera, a large gap suggests knee is caving in
    knee_toe_diff = abs(f_knee[0] - f_foot[0])
    if knee_toe_diff > 0.08:
        feedback.append(f"{'Left' if front=='LEFT' else 'Right'} knee drifting — keep it aligned over your toes")

    # ── Back knee drop ───────────────────────────────────────────────────────
    # back knee y should be relatively close to ground (high y value in image)
    if b_knee[1] < b_ankle[1] - 0.15:
        feedback.append("Drop your back knee lower — aim for just above the floor")

    # ── Torso upright ────────────────────────────────────────────────────────
    if torso_angle < 70:
        feedback.append("Stand tall — keep your torso upright, don't lean forward")

    form_ok = len(feedback) == 0
    if form_ok:
        feedback.append("Excellent lunge form!")

    return form_ok, feedback
