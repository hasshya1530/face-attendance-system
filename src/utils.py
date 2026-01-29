import cv2
import numpy as np
import time


def get_camera():
    """
    Opens the system camera with macOS compatibility.
    Tries multiple camera indices for reliability.
    """
    for index in [0, 1]:
        cam = cv2.VideoCapture(index, cv2.CAP_AVFOUNDATION)
        if cam.isOpened():
            time.sleep(1)  # Allow camera to warm up
            return cam

    raise RuntimeError(
        "Camera not accessible. Please allow camera access in System Settings → Privacy & Security → Camera."
    )


def detect_spoof(frame_history, motion_threshold=2.0):
    """
    Basic liveness / spoof detection using frame variation.
    
    Logic:
    - Collect multiple consecutive frames
    - Compute pixel-wise difference
    - Reject static or frozen frames (photo / replay attack)

    Returns:
    True  → Live face detected
    False → Possible spoof
    """

    if len(frame_history) < 5:
        return False

    diffs = []
    for i in range(1, len(frame_history)):
        diff = np.mean(
            np.abs(frame_history[i].astype("float") - frame_history[i - 1].astype("float"))
        )
        diffs.append(diff)

    avg_motion = np.mean(diffs)

    return avg_motion > motion_threshold
