import streamlit as st
from datetime import datetime
import random
import cv2
import numpy as np
from pyzbar.pyzbar import decode

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

# ---------- CSS ----------
st.markdown("""
<style>
body {background:#0b1220;font-family:Inter;}
#MainMenu, footer, header {visibility:hidden;}

.block-container {max-width:1200px;padding:20px;margin:auto;}

.header {
    background: linear-gradient(135deg,#1a73e8,#4285f4);
    padding:25px;border-radius:20px;color:white;
}

.balance {
    background:white;padding:22px;border-radius:16px;color:#202124;
}

.balance h2 {color:#1a73e8;}

.stButton button {
    background: transparent;
    border: none;
    color: white;
    font-size: 14px;
    padding: 10px;
}

.stButton button::first-line {
    display: block;
    font-size: 24px;
    background: #e8f0fe;
    color: black;
    border-radius: 16px;
    width: 55px;
    height: 55px;
    line-height: 55px;
    margin: auto;
    margin-bottom: 6px;
}

.card {
    background:white;padding:16px;border-radius:14px;margin-top:12px;color:#202124;
}

.popup {
    background:white;
    padding:20px;
    border-radius:16px;
    margin-top:20px;
    box-shadow:0 10px 30px rgba(0,0,0,0.4);
}
</style>
""", unsafe_allow_html=True)

# ---------- NAV ----------
home, pay, history, profile = st.tabs(["🏠 Home", "💸 Pay", "📊 History", "👤 Profile"])

# ---------- HOME ----------
with home:

    col1, col2 = st.columns([2.2, 1])

    with col1:
        st.markdown(f"""
        <div class="header">
            <h3>Hello, {st.session_state.profile['name']}</h3>
            <p>Welcome back</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 💸 Quick Actions")

        c1, c2, c3, c4, c5 = st.columns(5)

        if c1.button("📷\nScan QR"):
            st.session_state.popup = "scan"

        if c2.button("👤\nPay Anyone"):
            st.session_state.popup = "pay"

        if c3.button("🏦\nBank Transfer"):
            st.session_state.popup = "bank"

        if c4.button("⚡\nRecharge"):
            st.session_state.popup = "recharge"

        if c5.button("🧾\nPay Bills"):
            st.session_state.popup = "bills"

        # ---------- POPUPS ----------
        if st.session_state.popup:

            st.markdown('<div class="popup">', unsafe_allow_html=True)

            if st.button("❌ Close"):
                st.session_state.popup = None
                st.rerun()

            # ---------- ADVANCED QR SCANNER ----------
            if st.session_state.popup == "scan":

                st.subheader("Live QR Scanner")

                start = st.checkbox("Start Scanner")
                frame_window = st.empty()
                status = st.empty()

                if start:
                    cap = cv2.VideoCapture(0)

                    while start:
                        ret, frame = cap.read()
                        if not ret:
                            status.error("Camera error")
                            break

                        frame = cv2.flip(frame, 1)
                        h, w, _ = frame.shape

                        # Scan box
                        size = 250
                        x1, y1 = w//2 - size//2, h//2 - size//2
                        x2, y2 = w//2 + size//2, h//2 + size//2

                        # Dark overlay
                        overlay = frame.copy()
                        cv2.rectangle(overlay, (0,0),(w,h),(0,0,0),-1)
                        frame = cv2.addWeighted(overlay,0.5,frame,0.5,0)

                        # Clear center
                        frame[y1:y2, x1:x2] = overlay[y1:y2, x1:x2]

                        # Draw scan border
                        color = (255,255,255)

                        decoded = decode(frame)
                        detected = False

                        for obj in decoded:
                            x, y, w_box, h_box = obj.rect

                            if x1 < x < x2 and y1 < y < y2:
                                detected = True
                                color = (0,255,0)

                                data = obj.data.decode("utf-8")
                                status.success(f"QR Detected: {data}")

                                cv2.rectangle(frame,(x,y),(x+w_box,y+h_box),(0,255,0),2)

                            else:
                                color = (0,0,255)
                                status.warning("Move QR into scan box")

                        cv2.rectangle(frame,(x1,y1),(x2,y2),color,3)

                        frame_window.image(frame, channels="BGR")

                    cap.release()

            # ---------- PAY ----------
            elif st.session_state.popup == "pay":
                st.subheader("Pay Anyone")

                upi = st.text_input("UPI ID")
                amt = st.number_input("Amount ₹", min_value=1.0)

                if st.button("Send"):
                    if amt > st.session_state.balance:
                        st.error("Insufficient balance")
                    else:
                        st.session_state.balance -= amt
                        st.success("Payment Successful")

            # ---------- RECHARGE ----------
            elif st.session_state.popup == "recharge":
                st.subheader("Recharge")

                num = st.text_input("Mobile")
                amt = st.number_input("Amount", min_value=10.0)

                if st.button("Recharge"):
                    if amt > st.session_state.balance:
                        st.error("Insufficient balance")
                    else:
                        st.session_state.balance -= amt
                        st.success("Recharge Done")

            st.markdown('</div>', unsafe_allow_html=True)

        # ---------- RECENT ----------
        st.markdown("### 📊 Recent Activity")

        for tx in st.session_state.transactions[:5]:
            st.markdown(f"""
            <div class="card">
                <b>{tx['to']}</b>
                <span style="float:right;color:red;">₹{tx['amt']:,.2f}</span>
                <div style="font-size:12px;color:gray;">{tx['date']}</div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="balance">
            <div>Available Balance</div>
            <h2>₹{st.session_state.balance:,.2f}</h2>
            <small>{st.session_state.profile['bank']} • {st.session_state.profile['mask']}</small>
        </div>
        """, unsafe_allow_html=True)
