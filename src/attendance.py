import pandas as pd
from datetime import datetime
import os

FILE = "data/attendance.csv"


def mark_attendance(name, action):
    """
    Smart attendance logic per user per day.

    action:
    - "IN"  → Punch-In
    - "OUT" → Punch-Out
    """

    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    # ------------------ LOAD / INIT FILE ------------------
    if not os.path.exists(FILE) or os.path.getsize(FILE) == 0:
        df = pd.DataFrame(columns=["Name", "Date", "Punch-In", "Punch-Out"])
    else:
        df = pd.read_csv(FILE)

    today = df[(df["Name"] == name) & (df["Date"] == date)]

    # ===================== PUNCH-IN =====================
    if action == "IN":

        if not today.empty:
            punch_in = today.iloc[0]["Punch-In"]
            punch_out = today.iloc[0]["Punch-Out"]

            if pd.notna(punch_in) and pd.notna(punch_out):
                return "ℹ️ Attendance already completed for today"

            if pd.notna(punch_in) and pd.isna(punch_out):
                return "ℹ️ Punch-In already done, Punch-Out pending"

        # Fresh punch-in
        if today.empty:
            df.loc[len(df)] = [name, date, time, None]
        else:
            df.loc[today.index[0], "Punch-In"] = time

        df.to_csv(FILE, index=False)
        return "✅ Punch-In successful"

    # ===================== PUNCH-OUT =====================
    if action == "OUT":

        if today.empty or pd.isna(today.iloc[0]["Punch-In"]):
            return "❌ Punch-In required before Punch-Out"

        if pd.notna(today.iloc[0]["Punch-Out"]):
            return "ℹ️ Punch-Out already completed"

        df.loc[today.index[0], "Punch-Out"] = time
        df.to_csv(FILE, index=False)
        return "✅ Punch-Out successful"

    # ===================== INVALID =====================
    return "❌ Invalid action"
