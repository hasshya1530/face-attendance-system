import streamlit as st
import subprocess
import os
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Face Authentication Attendance",
    page_icon="🧠",
    layout="centered"
)

# ---------------- STYLES ----------------
st.markdown("""
<style>
.big-title {
    font-size: 36px;
    font-weight: 700;
}
.subtitle {
    font-size: 18px;
    color: #aaaaaa;
}
.card {
    padding: 20px;
    border-radius: 14px;
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.12);
    color: #eaeaea;
    backdrop-filter: blur(8px);
}
.status-success {
    padding: 15px;
    background-color: #e6fffa;
    border-left: 6px solid #38b2ac;
    color: #065f5b;
}
.status-error {
    padding: 15px;
    background-color: #ffe6e6;
    border-left: 6px solid #e53e3e;
    color: #7a1c1c;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown("<div class='big-title'>🧠 Face Authentication Attendance</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Secure, AI-powered Punch-In / Punch-Out System</div>", unsafe_allow_html=True)

st.divider()

# ---------------- INFO CARD ----------------
st.markdown("""
<div class="card">
<b>How it works</b><br><br>
• Register your face using the live camera<br>
• Authenticate for Punch-In or Punch-Out<br>
• Maximum <b>3 attempts</b> per action<br>
• Prevents duplicate attendance & spoofing attempts
</div>
""", unsafe_allow_html=True)

st.divider()

# ---------------- ENV CHECK ----------------
IS_DEPLOYED = os.getenv("STREAMLIT_SERVER_RUNNING") is not None

if IS_DEPLOYED:
    st.warning("⚠️ Camera access is disabled on deployed platforms.")
    st.info("Run locally to enable face authentication.")
else:
    st.success("✅ Local environment detected — camera enabled")

st.divider()

# ---------------- ACTIONS ----------------
st.subheader("🎯 Actions")

col1, col2, col3 = st.columns(3)

PYTHON_PATH = "/Library/Frameworks/Python.framework/Versions/3.13/bin/python3"

# -------- REGISTER FACE --------
with col1:
    if st.button("📝 Register Face", use_container_width=True):
        if IS_DEPLOYED:
            st.error("Camera not available in deployed mode.")
        else:
            with st.spinner("📸 Registering face — look at the camera"):
                subprocess.run([PYTHON_PATH, "src/register_face.py"])
            st.markdown(
                "<div class='status-success'>✅ Face registration completed successfully</div>",
                unsafe_allow_html=True
            )

# -------- PUNCH IN --------
with col2:
    if st.button("🟢 Punch-In", use_container_width=True):
        if IS_DEPLOYED:
            st.error("Camera not available in deployed mode.")
        else:
            with st.spinner("🔐 Authenticating for Punch-In"):
                subprocess.run([
                    PYTHON_PATH,
                    "src/recognize_face.py",
                    "punch_in"
                ])


# -------- PUNCH OUT --------
with col3:
    if st.button("🔴 Punch-Out", use_container_width=True):
        if IS_DEPLOYED:
            st.error("Camera not available in deployed mode.")
        else:
            with st.spinner("🔐 Authenticating for Punch-Out"):
                subprocess.run([
                    PYTHON_PATH,
                    "src/recognize_face.py",
                    "punch_out"
                ])

st.divider()

# ---------------- ATTENDANCE TABLE ----------------
st.subheader("📊 Attendance Records")

attendance_file = "data/attendance.csv"

if os.path.exists(attendance_file):
    try:
        df = pd.read_csv(attendance_file)
        st.dataframe(df, use_container_width=True)
    except Exception:
        st.warning("Attendance file exists but is empty.")
else:
    st.info("No attendance records available yet.")

st.divider()

# ---------------- FOOTER ----------------
st.caption(
    "Built using InsightFace (ArcFace), ONNX Runtime & OpenCV • Secure • macOS Compatible"
)
