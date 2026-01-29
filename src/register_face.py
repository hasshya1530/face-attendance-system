import os
import pickle
import numpy as np
import cv2
from insightface.app import FaceAnalysis
from utils import get_camera

# Ensure data folder exists
os.makedirs("data", exist_ok=True)

data_path = "data/embeddings.pkl"

# Load existing embeddings safely
if os.path.exists(data_path) and os.path.getsize(data_path) > 0:
    with open(data_path, "rb") as f:
        data = pickle.load(f)
else:
    data = {}

# Ask user name
name = input("Enter user name: ").strip()

# Check if already registered
if name in data:
    print(f"⚠️ {name} is already registered")
    exit(0)

# Initialize InsightFace
app = FaceAnalysis(
    name="buffalo_l",
    providers=["CPUExecutionProvider"]
)
app.prepare(ctx_id=0, det_size=(640, 640))

cam = get_camera()
embeddings = []

print("Look at the camera. Capturing face samples...")

# Capture 15 face embeddings
while len(embeddings) < 15:
    ret, frame = cam.read()
    if not ret:
        continue

    faces = app.get(frame)
    if faces:
        embeddings.append(faces[0].embedding)
        print(f"Captured {len(embeddings)}/15")

    cv2.imshow("Register Face", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cam.release()
cv2.destroyAllWindows()

# Average embedding
avg_embedding = np.mean(embeddings, axis=0)

# Save new user
data[name] = avg_embedding

with open(data_path, "wb") as f:
    pickle.dump(data, f)

print(f"✅ {name} registered successfully")
