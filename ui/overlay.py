"""
ui/overlay.py — draws the HUD on top of the webcam feed
"""

import cv2
import numpy as np


# ── Color palette (BGR) ───────────────────────────────────────────────────────
GREEN  = (80, 220, 80)
RED    = (60, 60, 230)
WHITE  = (255, 255, 255)
BLACK  = (0, 0, 0)
DARK   = (20, 20, 20)
YELLOW = (0, 215, 255)
TEAL   = (200, 200, 50)


def _alpha_rect(frame, x, y, w, h, color, alpha=0.55):
    """Draw a semi-transparent filled rectangle."""
    overlay = frame.copy()
    cv2.rectangle(overlay, (x, y), (x + w, y + h), color, -1)
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)


def draw_overlay(frame, exercise_name, form_ok, feedback):
    """Draw the status banner and feedback text on the frame."""
    h, w = frame.shape[:2]

    # ── Top status bar ────────────────────────────────────────────────────────
    bar_color = (30, 130, 30) if form_ok else (30, 30, 140)
    _alpha_rect(frame, 0, 0, w, 60, bar_color, alpha=0.75)

    # Exercise name
    label = exercise_name if exercise_name else "Select an exercise (press 1-4)"
    cv2.putText(frame, label, (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1.1, WHITE, 2, cv2.LINE_AA)

    # Form status indicator (right side)
    status_text  = "✓  GOOD FORM" if form_ok else "⚠  ADJUST FORM"
    status_color = GREEN if form_ok else YELLOW
    text_size    = cv2.getTextSize(status_text, cv2.FONT_HERSHEY_SIMPLEX, 0.9, 2)[0]
    cv2.putText(frame, status_text, (w - text_size[0] - 20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, status_color, 2, cv2.LINE_AA)

    # ── Feedback panel (bottom-left) ──────────────────────────────────────────
    if feedback:
        panel_h = len(feedback) * 34 + 20
        panel_y = h - panel_h - 10
        _alpha_rect(frame, 10, panel_y, w // 2 + 100, panel_h, DARK, alpha=0.70)

        for i, line in enumerate(feedback):
            bullet_color = GREEN if form_ok else RED
            y_pos = panel_y + 28 + i * 34
            # Bullet dot
            cv2.circle(frame, (28, y_pos - 6), 6, bullet_color, -1)
            cv2.putText(frame, line, (44, y_pos),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.62, WHITE, 1, cv2.LINE_AA)

    # ── Bottom hint bar ───────────────────────────────────────────────────────
    _alpha_rect(frame, 0, h - 28, w, 28, DARK, alpha=0.65)
    cv2.putText(frame, "M = menu   Q = quit", (w - 220, h - 8),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (160, 160, 160), 1, cv2.LINE_AA)


def draw_menu(frame, exercises: dict):
    """Draw the exercise selection menu."""
    h, w = frame.shape[:2]
    menu_w, menu_h = 280, len(exercises) * 50 + 60
    mx = (w - menu_w) // 2
    my = (h - menu_h) // 2

    _alpha_rect(frame, mx, my, menu_w, menu_h, DARK, alpha=0.85)
    cv2.rectangle(frame, (mx, my), (mx + menu_w, my + menu_h), TEAL, 2)

    cv2.putText(frame, "CHOOSE EXERCISE", (mx + 28, my + 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.65, TEAL, 2, cv2.LINE_AA)

    for i, (key, (name, _)) in enumerate(exercises.items()):
        y = my + 65 + i * 50
        cv2.putText(frame, f"[{key}]  {name}", (mx + 28, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.72, WHITE, 1, cv2.LINE_AA)
