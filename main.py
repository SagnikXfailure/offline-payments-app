import streamlit as st
from datetime import datetime
import random
import time

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

            # ---------- SMOOTH QR UI ----------
            if st.session_state.popup == "scan":

                st.subheader("QR Scanner")

                img = st.camera_input("Scan QR")

                progress = st.progress(0)
                status = st.empty()

                if img:
                    for i in range(100):
                        time.sleep(0.01)
                        progress.progress(i + 1)

                    # Fake detection logic (since no decoder)
                    if random.choice([True, False]):
                        status.success("✅ QR Detected Successfully")
                        st.balloons()
                    else:
                        status.error("❌ Improper QR Position - Adjust and Retry")

                st.caption("Align QR inside scan zone")

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
