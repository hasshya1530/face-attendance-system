import streamlit as st
import os
import pandas as pd

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Face Authentication Attendance",
    layout="centered"
)

ATTENDANCE_FILE = "data/attendance.csv"

# Detect cloud environment
IS_CLOUD = os.getenv("STREAMLIT_SERVER_RUNNING") is not None

# ---------------- UI ----------------
st.title("🧠 Face Authentication Attendance System")
st.caption("AI-powered attendance using face recognition")

st.markdown("---")

st.markdown("### 📌 Project Overview")
st.markdown("""
This system uses **deep-learning-based face recognition** to:
- Register a user's face
- Authenticate identity
- Automatically manage **Punch-In / Punch-Out**
- Prevent duplicate or invalid attendance entries

The biometric pipeline runs **locally** due to cloud security restrictions.
""")

st.markdown("---")

st.markdown("### ⚙️ System Capabilities")
st.markdown("""
✔ Pretrained face recognition model (InsightFace – ArcFace)  
✔ Spoof-resistant face embeddings  
✔ Daily attendance state management  
✔ Clean CSV-based logging  
✔ macOS & Python 3.13 compatible  
""")

st.markdown("---")

# ---------------- DEPLOYMENT NOTICE ----------------
if IS_CLOUD:
    st.warning("🚫 Live camera access is disabled on cloud platforms.")
    st.info(
        "For security reasons, webcam access cannot run on cloud servers.\n\n"
        "👉 Please run this project locally to use face registration and attendance marking.\n\n"
        "📽 A demo video is provided in the GitHub repository."
    )
else:
    st.success("✅ Local environment detected. Camera access is enabled.")

st.markdown("---")

# ---------------- ACTION BUTTONS ----------------
st.markdown("### 🎯 Actions")

col1, col2 = st.columns(2)

with col1:
    st.button("📝 Register Face", disabled=IS_CLOUD)

with col2:
    st.button("🕵️ Authenticate & Mark Attendance", disabled=IS_CLOUD)

if IS_CLOUD:
    st.caption("Buttons are disabled in cloud deployment.")

st.markdown("---")

# ---------------- ATTENDANCE TABLE ----------------
st.markdown("### 📂 Attendance Records")

if os.path.exists(ATTENDANCE_FILE) and os.path.getsize(ATTENDANCE_FILE) > 0:
    df = pd.read_csv(ATTENDANCE_FILE)
    st.dataframe(df, use_container_width=True)
else:
    st.info("No attendance records available.")

st.markdown("---")

# ---------------- FOOTER ----------------
st.caption(
    "⚠️ Note: Face recognition is demonstrated locally due to platform limitations. "
    "This deployment showcases the UI, workflow, and system design."
)
