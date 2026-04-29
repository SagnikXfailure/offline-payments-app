import streamlit as st
from datetime import datetime
import random
import time
import numpy as np
from PIL import Image

# QR detection libs
from pyzbar.pyzbar import decode
import cv2

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="PayFlow", page_icon="💳", layout="wide")

# ---------- SESSION ----------
if "balance" not in st.session_state:
    st.session_state.balance = 50000.0

if "transactions" not in st.session_state:
    st.session_state.transactions = []

if "profile" not in st.session_state:
    st.session_state.profile = {
        "name": "Abhishek",
        "upi": "abhi@okicici",
        "bank": "ICICI Bank",
        "mask": "XXXX 1234"
    }

if "popup" not in st.session_state:
    st.session_state.popup = None

# ---------- NAV ----------
home, pay, history, profile = st.tabs(["🏠 Home", "💸 Pay", "📊 History", "👤 Profile"])

# ---------- HOME ----------
with home:

    col1, col2 = st.columns([2.2, 1])

    with col1:
        st.markdown("### 💸 Quick Actions")

        c1, c2, c3, c4, c5 = st.columns(5)

        if c1.button("📷\nScan QR"):
            st.session_state.popup = "scan"

        # ---------- POPUP ----------
        if st.session_state.popup == "scan":

            st.markdown("## 📷 QR Scanner")

            img_file = st.camera_input("Capture QR")

            status = st.empty()

            if img_file:

                image = Image.open(img_file)
                frame = np.array(image)

                # Convert to grayscale
                gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

                # Decode QR
                decoded_objects = decode(gray)

                if not decoded_objects:
                    status.error("❌ Not a QR Code or unreadable")
                else:
                    for obj in decoded_objects:

                        data = obj.data.decode("utf-8")
                        x, y, w, h = obj.rect

                        # ---------- VALIDATION RULES ----------

                        # 1. Size check
                        if w < 50 or h < 50:
                            status.warning("⚠️ QR too small, move closer")
                            continue

                        # 2. Data check
                        if len(data) < 3:
                            status.error("❌ Invalid QR content")
                            continue

                        # 3. Format check (example for UPI)
                        if data.startswith("upi://"):
                            status.success(f"✅ Valid UPI QR\n\n{data}")
                        else:
                            status.success(f"✅ QR Detected\n\n{data}")

                        # Draw bounding box
                        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)

                st.image(frame)
