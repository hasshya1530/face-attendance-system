# Face Authentication Attendance System

## Overview
This project implements a **real-time face authentication–based attendance system** using a live camera feed.  
It allows users to **register their face**, **authenticate identity**, and automatically mark **Punch-In** and **Punch-Out** attendance.

The system is designed to be **lightweight, reliable, and compatible with macOS**, using modern deep-learning–based face embeddings.

---

## Features
- Live face registration using camera
- Face authentication using deep learning embeddings
- Automatic Punch-In and Punch-Out logic
- Prevents duplicate attendance entries
- Multi-user support
- CSV-based attendance storage
- Basic spoof prevention (frame variation check)
- Compatible with modern Python versions (Python 3.13)

---

## Tech Stack
- **Python 3.13**
- **InsightFace (ArcFace embeddings)**
- **ONNX Runtime**
- **OpenCV**
- **NumPy**
- **Pandas**
- **Scikit-learn**

---

## Project Structure
# Face Authentication Attendance System

## Overview
This project implements a **real-time face authentication–based attendance system** using a live camera feed.  
It allows users to **register their face**, **authenticate identity**, and automatically mark **Punch-In** and **Punch-Out** attendance.

The system is designed to be **lightweight, reliable, and compatible with macOS**, using modern deep-learning–based face embeddings.

---

## Features
- Live face registration using camera
- Face authentication using deep learning embeddings
- Automatic Punch-In and Punch-Out logic
- Prevents duplicate attendance entries
- Multi-user support
- CSV-based attendance storage
- Basic spoof prevention (frame variation check)
- Compatible with modern Python versions (Python 3.13)

---

## Tech Stack
- **Python 3.13**
- **InsightFace (ArcFace embeddings)**
- **ONNX Runtime**
- **OpenCV**
- **NumPy**
- **Pandas**
- **Scikit-learn**

---

## Project Structure
face_attendance_system/
├── src/
│ ├── register_face.py # Register new users
│ ├── recognize_face.py # Authenticate & mark attendance
│ ├── attendance.py # Punch-In / Punch-Out logic
│ └── utils.py # Camera utility
│
├── data/
│ ├── embeddings.pkl # Stored face embeddings
│ └── attendance.csv # Attendance records
│
├── requirements.txt
└── README.md
# face-attendance-system
