import numpy as np

def basic_liveness(frames, threshold=30):
    if len(frames) < 2:
        return False
    diff = np.mean(np.abs(frames[-1].astype(int) - frames[-2].astype(int)))
    return diff > threshold
