"""
exercises/squat.py

Checks:
  ✓ Knee angle 70–110° at bottom (deep enough, not caving)
  ✓ Hip hinge present (hip below knee level at bottom)
  ✓ Knee tracking over toes (no inward collapse)
  ✓ Torso not excessively forward-leaning
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import get_coords, angle_between


def analyze_squat(landmarks, PoseLandmark):
    """
    Returns:
        form_ok  (bool)  – True when all checks pass
        feedback (list)  – list of instruction strings for the user
    """
    feedback = []

    # ── Grab key landmarks ───────────────────────────────────────────────────
    l_hip    = get_coords(landmarks, PoseLandmark, "LEFT_HIP")
    l_knee   = get_coords(landmarks, PoseLandmark, "LEFT_KNEE")
    l_ankle  = get_coords(landmarks, PoseLandmark, "LEFT_ANKLE")
    l_foot   = get_coords(landmarks, PoseLandmark, "LEFT_FOOT_INDEX")

    r_hip    = get_coords(landmarks, PoseLandmark, "RIGHT_HIP")
    r_knee   = get_coords(landmarks, PoseLandmark, "RIGHT_KNEE")
    r_ankle  = get_coords(landmarks, PoseLandmark, "RIGHT_ANKLE")

    l_shoulder = get_coords(landmarks, PoseLandmark, "LEFT_SHOULDER")

    # ── Compute angles ───────────────────────────────────────────────────────
    l_knee_angle = angle_between(l_hip, l_knee, l_ankle)
    r_knee_angle = angle_between(r_hip, r_knee, r_ankle)
    avg_knee     = (l_knee_angle + r_knee_angle) / 2

    # Torso lean: angle at hip between shoulder and knee
    torso_angle  = angle_between(l_shoulder, l_hip, l_knee)

    # ── Standing (not in squat yet) ──────────────────────────────────────────
    if avg_knee > 160:
        feedback.append("Stand with feet shoulder-width apart, toes slightly out")
        feedback.append("Begin your squat when ready")
        return True, feedback          # neutral standing = OK

    # ── In squat range ───────────────────────────────────────────────────────

    # 1. Depth check
    if avg_knee > 110:
        feedback.append("Go deeper — bend your knees more toward 90°")

    # 2. Don't go past safe range
    elif avg_knee < 60:
        feedback.append("Too deep — raise up slightly to protect your knees")

    # 3. Knee cave (left knee drifts inward relative to foot)
    if l_knee[0] > l_foot[0] + 0.05:          # x-axis: knee too far right (inward)
        feedback.append("Left knee caving in — push it out over your toes")
    if r_knee[0] < r_ankle[0] - 0.05:
        feedback.append("Right knee caving in — push it out over your toes")

    # 4. Excessive forward lean
    if torso_angle < 40:
        feedback.append("Chest up — don't lean too far forward")

    # 5. Hip depth (hips should drop below parallel at bottom)
    if avg_knee < 100 and l_hip[1] < l_knee[1]:   # y increases downward in image
        feedback.append("Drop your hips lower — aim for parallel or below")

    form_ok = len(feedback) == 0
    if form_ok:
        feedback.append("Great squat form! Keep it up.")

    return form_ok, feedback
