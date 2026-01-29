import sys
import pickle
import cv2
import numpy as np
import os
from sklearn.metrics.pairwise import cosine_similarity
from insightface.app import FaceAnalysis
from utils import get_camera
from attendance import mark_attendance

# ================== ACTION MODE ==================
if len(sys.argv) < 2:
    print("❌ Action not provided (punch_in / punch_out)")
    sys.exit(1)

RAW_ACTION = sys.argv[1].lower()

if RAW_ACTION == "punch_in":
    ACTION = "IN"
elif RAW_ACTION == "punch_out":
    ACTION = "OUT"
else:
    print("❌ Invalid action. Use punch_in or punch_out")
    sys.exit(1)

print(f"\n🔐 Authentication Started for {ACTION}")
print("👉 Look at the camera...")

# ================== LOAD EMBEDDINGS ==================
if not os.path.exists("data/embeddings.pkl"):
    print("❌ No registered users found")
    sys.exit(1)

with open("data/embeddings.pkl", "rb") as f:
    known_faces = pickle.load(f)

# ================== FACE MODEL ==================
app = FaceAnalysis(
    name="buffalo_l",
    providers=["CPUExecutionProvider"]
)
app.prepare(ctx_id=0, det_size=(640, 640))

# ================== CAMERA ==================
cam = get_camera()

THRESHOLD = 0.45
MAX_ATTEMPTS = 3
attempts = 0
prev_embedding = None

while True:
    ret, frame = cam.read()
    if not ret:
        continue

    faces = app.get(frame)

    if not faces:
        cv2.imshow("Authentication", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        continue

    # ------------------ CURRENT FACE ------------------
    emb = faces[0].embedding.reshape(1, -1)

    # ------------------ BASIC SPOOF CHECK ------------------
    if prev_embedding is not None:
        motion_score = cosine_similarity(emb, prev_embedding)[0][0]
        if motion_score > 0.99:
            print("⚠️ Possible spoof detected (no head movement)")
            attempts += 1
            if attempts >= MAX_ATTEMPTS:
                print("🚫 Too many failed attempts. Access blocked.")
                break
            prev_embedding = emb
            continue

    prev_embedding = emb

    # ------------------ MATCHING ------------------
    best_score = 0
    best_name = None

    for name, saved_emb in known_faces.items():
        saved_emb = np.array(saved_emb).reshape(1, -1)
        score = cosine_similarity(emb, saved_emb)[0][0]

        if score > best_score:
            best_score = score
            best_name = name

    # ------------------ DECISION ------------------
    if best_score >= THRESHOLD:
        message = mark_attendance(best_name, ACTION)
        print(f"👤 {best_name} → {message}")
        break
    else:
        print("❌ Face not recognized")
        attempts += 1
        if attempts >= MAX_ATTEMPTS:
            print("🚫 Too many failed attempts. Access blocked.")
            break

    cv2.imshow("Authentication", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cam.release()
cv2.destroyAllWindows()
